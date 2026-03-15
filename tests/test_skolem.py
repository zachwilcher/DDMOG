import unittest
from magicutils.skolem import skolem, langford

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
    
    def test_langford(self):
        for d in range(3, 100):
            for n in range(2 * d - 1, 2 * d - 1 + 100):
                necessary_conditions = \
                (n > 0) and (d > 0) and (n >= (2 * d - 1)) and (
                        (((n % 4 == 0) or (n % 4 == 1)) and (d % 2 == 1))
                    or  (((n % 4 == 0) or (n % 4 == 3)) and (d % 2 == 0))
                )
                if not necessary_conditions:
                    continue
                if not ((n % 4 == 0)):
                    continue
                pairs = langford(n,d)

                differences = [False] * n
                for (a,b) in pairs:
                    index = b - a - d
                    differences[index] = True
                test_passed = all(differences)
                if not test_passed:
                    print(pairs)
                    print(n,d)
                    print(differences)
                self.assertTrue(all(differences))



            