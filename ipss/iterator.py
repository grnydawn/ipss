# coding: utf-8

from __future__ import unicode_literals, print_function, division

import sys
import abc
from math import ceil, factorial

PY3 = sys.version_info >= (3, 0)

if PY3:
    Object = abc.ABCMeta("Object", (object,), {})
    from functools import reduce
    long = int
else:
    Object = abc.ABCMeta("Object".encode("utf-8"), (object,), {})

INF = float("inf")
NAN = float("nan")

class InfinityError(Exception):
    pass

class Iterator(Object):

    @abc.abstractmethod
    def __init__(self, *vargs, **kwargs):
        pass

    @abc.abstractmethod
    def getitem(self, key):
        pass

    def _item(self, k):
        k = self._validate_key(k)

        if k < self._len:
            return self.getitem(k)
        else:
            clsname = self.__class__.__name__
            raise IndexError("%s index out of range"%clsname)

    def __getitem__(self, key):

        if isinstance(key, slice):
            start = key.start if key.start else 0
            stop = key.stop if key.stop else self._len
            step = key.step if key.step else 1
            result = []
            for idx in range(start, stop, step):
                result.append(self._item(idx))
            return tuple(result)
        else:
            return self._item(key)

    def index(self, val):
        raise NotImplementedError()

    def __len__(self):
        return self._len

    def __iter__(self):

        self._key = 0
        return self

    def __next__(self):

        if self._len == INF or self._key < self._len:
            val = self.getitem(self._key)
            self._key += 1
            return val
        else:
            raise StopIteration

    def next(self):
        return self.__next__()

    def get(self, key, *vargs):
        val = self.__getitem__(key)
        if val is not None:
            return val
        elif vargs:
            return vargs[0]
        else:
            return None

    def _validate_key(self, key):

        if not isinstance(key, (int, long)):
            raise TypeError("Key should be 'int' or 'long' type: %s"%type(key))

        if key < 0:
            if self._len == INF:
                raise TypeError("Negative key for infinite iterator: %d"%key)
            return self._len + key
        elif self._len != INF and key >= self._len:
            raise IndexError("index '%d' is out of bound"%key)

        return key

    def _validate_iterable(self, iterable):

        if isinstance(iterable, Iterator):
            return iterable
        elif hasattr(iterable, "__len__"):
            return Wrapper(iterable)
        else:
            clsname = iterable.__class__.__name__
            raise TypeError("'%s' does not support len() method."%clsname)

class Wrapper(Iterator):

    def __init__(self, iterable):

        self._tuple = tuple(iterable)
        self._len = len(self._tuple)

    def getitem(self, key):

        return self._tuple[key]
        
class Range(Iterator):

    def __init__(self, *vargs):

        if len(vargs) == 1:
            self._start, self._stop, self._step = 0, vargs[0], 1
        elif len(vargs) == 2:
            self._start, self._stop, self._step = vargs[0], vargs[1], 1
        elif len(vargs) == 3:
            self._start, self._stop, self._step = vargs[0], vargs[1], vargs[2]
        else:
            raise Exception("The number of arguments is not correct"
                            " for 'Range': " + str(vargs))

        if self._step == 0:
            raise ValueError("Range step argument must not be zero.")
        elif any(not isinstance(v, int) for v in(
                self._start, self._stop, self._step)):
            raise ValueError("Range arguments must be integer type.")

        _len = float(self._stop - self._start) / float(self._step)
        self._len = int(ceil(_len)) if _len > 0 else 0

    def getitem(self, key):

        val = self._start + self._step * key
        if ((self._step > 0 and val < self._stop) or
                (self._step < 0 and val > self._stop)):
            return val

class Count(Iterator):

    def __init__(self, start=0, step=1):

        if isinstance(start, int) and isinstance(step, int):
            self._start, self._step = start, step
        else:
            raise ValueError("Count arguments must be integer type.")

        self._len = INF

    def getitem(self, key):

        return self._start + self._step * key


class Cycle(Iterator):
       
    def __init__(self, iterable):

        self._iterable = self._validate_iterable(iterable)

        if isinstance(self._iterable, Iterator):
            if len(self._iterable) == INF:
                clsname = iterable.__class__.__name__
                raise TypeError("Can not cycle infinite iterator: '%s'."%
                    clsname)
        else:
            clsname = iterable.__class__.__name__
            raise TypeError("'%s' does not support len() method."%clsname)

        self._len = INF
        self._iterable_len = len(self._iterable)

    def getitem(self, key):

        if key >= self._iterable_len:
            key = key % self._iterable_len

        return self._iterable[key]


class Repeat(Iterator):

    def __init__(self, elem, times=None):

        self._elem = elem

        if isinstance(times, int) or times is None:
            self._times = times
        else:
            raise ValueError("Repeat times argument must be an"
                             " integer type or None.")

        if times is None:
            self._len = INF
        else:
            self._len = times
            
    def getitem(self, key):

        return self._elem

class Chain(Iterator):

    def __init__(self, *iterables):

        self._iterables = []
        for it in iterables:
            self._iterables.append(self._validate_iterable(it))

        self._iterable_lens = [len(it) for it in self._iterables]
        
        if any(_l == INF for _l in self._iterable_lens[:-1]):
            raise InfinityError("Infinity iterator can not be chained except the last.")

        if self._iterable_lens[-1] == INF:
            self._len = INF
        else:
            self._len = sum(self._iterable_lens)

    def getitem(self, key):

        accum_len = 0
        for _len, it in zip(self._iterable_lens, self._iterables):
            if key >= accum_len and key < accum_len + _len:
                return it[key - accum_len]
            accum_len += _len

class Product(Iterator):

    def __init__(self, *iterables):

        self._pools = []
        for it in iterables:
            self._pools.append(self._validate_iterable(it))

        self._pools.reverse()
        self._pool_lens = [len(it) for it in self._pools]
        self._dimension = len(self._pools)

        if any(_l == INF for _l in self._pool_lens):
            raise InfinityError("Product does not support infinity iterator.")

        self._len = reduce(lambda x, y: x*y, self._pool_lens)

    def getitem(self, key):

        product = [None]*self._dimension
        for dim, (_len, it) in enumerate(zip(self._pool_lens, self._pools)):
            product[self._dimension-dim-1] = it[key % _len]
            key = key // _len

        return tuple(product)

class Permutations(Iterator):

    def __init__(self, iterable, r=None):

        self._iterable = self._validate_iterable(iterable)

        self._n = len(self._iterable)

        if self._n == INF:
            raise InfinityError("Permutation do not support infinity iterator.")

        self._r = self._n if r is None else r
        if self._r > self._n:
            self._len = 0
        else:
            self._len = factorial(self._n) // factorial(self._n-self._r)

    def getitem(self, key):

        class Marker(object):
            def __init__(self, it):
                self.it = it
                self.size = len(it)
                self.used = []
            def pop(self, reverse=True):
                if reverse:
                    l = range(self.size-1, -1, -1)
                else:
                    l = range(self.size)
                for i in l:
                    if i in self.used:
                        continue
                    self.used.append(i)
                    return self.it[i]
            def remained(self):
                return len(self.used) < self.size

        if self._r > 0:
            reverse = True
            seqc = Marker(self._iterable)
            seqn = [seqc.pop(reverse=reverse)]
            divider= 2
            while seqc.remained():
                key, new_key= key//divider, key%divider
                seqn.insert(new_key, seqc.pop(reverse=reverse))
                divider+= 1

            return tuple(seqn)
        else:
            return tuple()

class Combinations(Iterator):

    def __init__(self, iterable, r):

        self._iterable = self._validate_iterable(iterable)

        self._n = len(self._iterable)

        if self._n == INF:
            raise InfinityError("Combination do not support infinity iterator.")

        self._r = r

        if r > self._n:
            self._len = 0
        else:
            self._len = self._nCr(self._n, self._r)

    def _nCr(self, n, r):
        return (factorial(n) // factorial(r) // factorial(n-r))

    def _kth(self, k, l, r):

        if r == 0:
            return []
        elif len(l) == r:
            return l
        else:
            i=self._nCr(len(l)-1, r-1)
            if k < i:
                return list(l[0:1]) + self._kth(k, l[1:], r-1)
            else:
                return list(self._kth(k-i, l[1:], r))

    def getitem(self, key):

        return tuple(self._kth(key, self._iterable, self._r))
