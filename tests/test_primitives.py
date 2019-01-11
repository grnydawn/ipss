
import unittest
from random import seed, randint

import ipss
import itertools as it

N = 10

class PrimitiveTests(unittest.TestCase):

    def setUp(self):
        seed(47)
        self.maxDiff = None

    def tearDown(self):
        pass

    def _nrandint(self, n, start=-N, stop=N):
        i = 0
        ints = []
        while i < n:
            ints.append(randint(start, stop))
            i += 1
        return ints

    def _iter_equals(self, iterable1, iterable2):
            idx = 0
            while idx < N:
                val = next(iterable1, None) 
                ref = next(iterable2, None) 
                if val is None and ref is None:
                    break
                self.assertEquals(val, ref)
                idx += 1

    def test_range(self):

        for _ in range(N):

            slc = (randint(-10, 10), randint(-N, N), randint(-5, 5))
            if slc[2] == 0:
                continue
            self._iter_equals(iter(ipss.Range(*slc)), iter(range(*slc)))

    def test_count(self):

        for _ in range(N):
            slc = (randint(-N, N), randint(-5, 5))
            self._iter_equals(iter(ipss.Count(*slc)), it.count(*slc))

    def test_cycle(self):

        for _ in range(N):
            iterable = self._nrandint(N)
            self._iter_equals(iter(ipss.Cycle(iterable)), it.cycle(iterable))

    def test_repeat(self):

        for _ in range(N):
            self._iter_equals(iter(ipss.Repeat(1)), it.repeat(1))


    def test_chain(self):

        for i in range(N):

            iterables = (self._nrandint(N), self._nrandint(N))
            self._iter_equals(iter(ipss.Chain(*iterables)), it.chain(*iterables))

            slc1 = (randint(-10, 10), randint(-N, N), randint(1, 5))
            slc2 = (randint(-10, 10), randint(-N, N), randint(1, 5))

            iterables = (ipss.Range(*slc1), self._nrandint(N))
            self._iter_equals(iter(ipss.Chain(*iterables)), it.chain(*iterables))

            iterables = (ipss.Range(*slc1), range(*slc2))
            self._iter_equals(iter(ipss.Chain(*iterables)), it.chain(*iterables))

            # This should fail as iterator of range does not have __len__ method.
            #iterables = (ipss.Range(*slc1), iter(range(*slc2)))
            #self._iter_equals(iter(ipss.Chain(*iterables)), it.chain(*iterables))

            iterables = (ipss.Range(*slc1), [1,2,3])
            self._iter_equals(iter(ipss.Chain(*iterables)), it.chain(*iterables))


    def test_product(self):

        for i in range(N):

            iterables = (self._nrandint(N), self._nrandint(N))
            self._iter_equals(iter(ipss.Product(*iterables)), it.product(*iterables))

            slc1 = (randint(-10, 10), randint(-N, N), randint(1, 5))
            slc2 = (randint(-10, 10), randint(-N, N), randint(1, 5))

            iterables = (ipss.Range(*slc1), self._nrandint(N))
            self._iter_equals(iter(ipss.Product(*iterables)), it.product(*iterables))

            iterables = (ipss.Range(*slc1), range(*slc2))
            self._iter_equals(iter(ipss.Chain(*iterables)), it.chain(*iterables))

#            # This should fail as iterator of range does not have __len__ method.
#            #iterables = (ipss.Range(*slc1), iter(range(*slc2)))
#            #self._iter_equals(iter(ipss.Chain(*iterables)), it.chain(*iterables))

            iterables = (ipss.Range(*slc1), [1,2,3])
            self._iter_equals(iter(ipss.Chain(*iterables)), it.chain(*iterables))



    def test_permutations(self):

        for i in range(1):

            l = self._nrandint(N)
            seq1 = [p for p in ipss.Permutations(l)]
            seq2 = [p for p in it.permutations(l)]

            for seq in seq1:
                #self.assertEquals(val, ref)
                assert seq in seq2
            #self._iter_equals(iter(ipss.Permutations(l)), it.permutations(l))

#            slc1 = (randint(-10, 10), randint(-N, N), randint(1, 5))
#            slc2 = (randint(-10, 10), randint(-N, N), randint(1, 5))
#
#            iterables = (ipss.Range(*slc1), self._nrandint(N))
#            self._iter_equals(iter(ipss.Product(*iterables)), it.product(*iterables))
#
#            iterables = (ipss.Range(*slc1), range(*slc2))
#            self._iter_equals(iter(ipss.Chain(*iterables)), it.chain(*iterables))
#
##            # This should fail as iterator of range does not have __len__ method.
##            #iterables = (ipss.Range(*slc1), iter(range(*slc2)))
##            #self._iter_equals(iter(ipss.Chain(*iterables)), it.chain(*iterables))
#
#            iterables = (ipss.Range(*slc1), [1,2,3])
#            self._iter_equals(iter(ipss.Chain(*iterables)), it.chain(*iterables))


test_classes = (PrimitiveTests,)
