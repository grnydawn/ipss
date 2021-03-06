
import unittest
from random import seed, randint

import ipss
import itertools as it

N = 6

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
                self.assertEqual(val, ref)
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

        for i in range(N):

            l = self._nrandint(N)

            seq1 = [p for p in ipss.Permutations(l)]
            seq2 = [p for p in it.permutations(l)]

            for seq in seq1:
                self.assertIn(seq, seq2)

        seq1 = [p for p in ipss.Permutations(l, 0)]
        seq2 = [p for p in it.permutations(l, 0)]

        for seq in seq1:
            self.assertIn(seq, seq2)

        seq1 = [p for p in ipss.Permutations(l, N)]
        seq2 = [p for p in it.permutations(l, N)]

        for seq in seq1:
            self.assertIn(seq, seq2)

        seq1 = [p for p in ipss.Permutations(l, N*2)]
        seq2 = [p for p in it.permutations(l, N*2)]

        for seq in seq1:
            self.assertIn(seq, seq2)

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


    def test_combinations(self):

        for i in range(N):

            l = self._nrandint(N)
            r = int(len(l)/2)
            self._iter_equals(iter(ipss.Combinations(l,r)), it.combinations(l,r))

        r = 0
        self._iter_equals(iter(ipss.Combinations(l,r)), it.combinations(l,r))

        r = len(l)
        self._iter_equals(iter(ipss.Combinations(l,r)), it.combinations(l,r))

        r = len(l)*2
        self._iter_equals(iter(ipss.Combinations(l,r)), it.combinations(l,r))

    def test_custom(self):

        loop1 = {"indvars": ('a', 'b', 'c')}
        loop2 = {"indvars": ('x', 'y', 'z')}
        loops = (loop1, loop2)

        xform1 = {"interchange": (1,2,3)}
        xform2 = {"unroll": (-1,-2,-3)}
        xforms = (xform1, xform2)
        search_space = (loops, xforms)

        search_generator = ipss.Product(*search_space)

        self.assertEqual(len(search_generator), 4)



test_classes = (PrimitiveTests,)

