
import unittest
from random import seed, randint

import ipss
import itertools as it

class PrimitiveTests(unittest.TestCase):

    def setUp(self):
        seed(47)

    def tearDown(self):
        pass

    def test_range(self):

        for _ in range(100):

            slc1 = (randint(-10, 10), randint(-100, 100), randint(-5, 5))
            if slc1[2] == 0:
                continue

            spc1 = list(ipss.Range(*slc1))
            rng1 = range(*slc1)

            self.assertEquals(spc1, rng1)

    def test_count(self):

        for _ in range(100):

            slc = (randint(-100, 100), randint(-5, 5))

            idx = 0
            ipsscount = iter(ipss.Count(*slc))
            itercount = it.count(*slc) 
            while idx < 100:
                val = next(ipsscount) 
                ref = next(itercount) 
                self.assertEquals(val, ref)
                idx += 1

#            spc = ipss.Count(*slc)
#
#            self.assertEquals(spc[5], slc[0] + slc[1]*5)
#
#    def test_cycle(self):
#
#        for _ in range(100):
#
#            slc = (randint(-100, 100), randint(-5, 5))
#
#            spc = ipss.Count(*slc)
#
#            self.assertEquals(spc[5], slc[0] + slc[1]*5)

test_classes = (PrimitiveTests,)
