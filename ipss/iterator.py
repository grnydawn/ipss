# coding: utf-8

from __future__ import unicode_literals, print_function

import sys
import abc
import math

PY3 = sys.version_info >= (3, 0)

if PY3:
    Object = abc.ABCMeta("Object", (object,), {})
else:
    Object = abc.ABCMeta("Object".encode("utf-8"), (object,), {})

INF = float("inf")
NAN = float("nan")

def _make_Iterator(iterable):
    import pdb; pdb.set_trace()

class Iterator(Object):

    @abc.abstractmethod
    def __init__(self, *vargs, **kwargs):
        pass

    @abc.abstractmethod
    def __getitem__(self, key):
        pass

    def index(self, val):
        raise NotImplementedError()

    def __len__(self):
        return self._len

    def __iter__(self):

        self._key = 0
        return self

    def __next__(self):

        if self._len == INF or self._key < self._len:
            _val = self.__getitem__(self._key)
            self._key += 1
            return _val
        else:
            raise StopIteration

    def next(self):
        return self.__next__()

    def get(self, key, *vargs):
        _val = self.__getitem__(key)
        if _val is not None:
            return _val
        elif vargs:
            return vargs[0]
        else:
            return None

    def _validate_key(self, key):

        if not isinstance(key, int):
            raise TypeError("Key should be 'int' type: %s"%type(key))

        if key < 0:
            if self._len == INF:
                raise TypeError("Negative key for infinite iterator: %d"%key)
            return self._len + key
        elif self._len != INF and key >= self._len:
            raise TypeError("Key is out of bound: %d."%key)

        return key

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
        self._len = int(math.ceil(_len)) if _len > 0 else 0

    def __getitem__(self, key):
        _val = self._start + self._step * self._validate_key(key)
        if ((self._step > 0 and key >= 0 and _val < self._stop) or
                (self._step < 0 and key >= 0 and _val > self._stop)):
            return _val
        else:
            return None


class Count(Iterator):

    def __init__(self, start=0, step=1):

        if isinstance(start, int) and isinstance(step, int):
            self._start, self._step = start, step
        else:
            raise ValueError("Count arguments must be integer type.")

        self._len = INF

    def __getitem__(self, key):

        return self._start + self._step * self._validate_key(key)


class Cycle(Iterator):

    def __init__(self, iterable):

        if isinstance(iterable, Iterator):
            if len(iterable) == INF:
                clsname = iterable.__class__.__name__
                raise TypeError("Can not cycle infinite iterator: '{}."%
                    clsname)
            self._iterable = iterable
        elif hasattr(iterable, "__len__"):
            self._iterable = _make_Iterator(iterable)
        else:
            clsname = iterable.__class__.__name__
            raise TypeError("'{} does not support len() method."%clsname)

        self._len = INF
        self._iterable_len = len(self._iterable)

    def __getitem__(self, key):

        key = self._validate_key(key)

        if key >= self._iterable_len:
            key = key % self._iterable_len

        return self._iterable[key]


#
#    # cycle('ABCD') --> A B C D A B C D A B C D ...
#    saved = []
#    for element in iterable:
#        yield element
#        saved.append(element)
#    while saved:
#        for element in saved:
#              yield element
#
#
