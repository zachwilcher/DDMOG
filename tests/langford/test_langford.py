import unittest
from langford import langford

class TestLangford(unittest.TestCase):
    def test_langford(self):
        for d in range(1, 100):
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
                self.assertTrue(all(differences))



            