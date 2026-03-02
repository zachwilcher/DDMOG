import unittest
import itertools
from magicutils.skolem import skolem, perfect_langford, near_skolem

class TestSkolemMethods(unittest.TestCase):
    def test_skolem(self):
        for n in range(1, 100):
            if (n % 4 != 0) and (n % 4 != 1):
                self.assertRaises(ValueError)
                continue
            pairs = skolem(n)
            differences = [False] * n
            for (a,b) in pairs:
                index = b - a - 1
                differences[index] = True
            self.assertTrue(all(differences))

    def test_perfect_langford(self):
        for n,d in itertools.product(range(1, 100), range(1,100)):
            necessary_conditions = \
                (n > 0) and (d > 0) and (n >= (2 * d - 1)) and (
                        (((n % 4 == 0) or (n % 4 == 1)) and (d % 2 == 1))
                    or  (((n % 4 == 2) or (n % 4 == 3)) and (d % 2 == 0))
                )
            if not necessary_conditions:
                self.assertRaises(ValueError)
            pairs = perfect_langford(n,d)
            differences = [False] * n

            for (a,b) in pairs:
                index = b - a - d
                differences[index] = True
            self.assertTrue(all(differences))
    
    def test_near_skolem(self):
        for n,m in itertools.product(range(8, 100, 8), range(1,100)):

            necessary_conditions = \
                (n > 0) and (m > 0) and (m <= n) and (
                       ((n % 4 == 0) and (m % 2 == 1))
                    or ((n % 4 == 1) and (m % 2 == 1))
                    or ((n % 4 == 2) and (m % 2 == 0))
                    or ((n % 4 == 3) and (m % 2 == 0))
                )
            
            if not necessary_conditions:
                self.assertRaises(ValueError)

            differences = [False] * n
            pairs = near_skolem(n,m)
            for (a,b) in pairs:
                index = b - a - 1
                differences[index] = True
            self.assertFalse(differences[m])
            differences[m] = True
            self.assertTrue(all(differences))
            


            