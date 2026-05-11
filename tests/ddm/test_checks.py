import unittest
import numpy as np
from ddm.checks import is_ddm, is_trivial, is_connected, is_balanced

class TestChecks(unittest.TestCase):

    def test_is_ddm(self):
        # verify a ddm labeling of the 4-spoke wheel
        A = np.array([[0, 0, 0, 0, 1],
                      [1, 0, 0, 1, 0],
                      [1, 0, 0, 1, 0],
                      [0, 0, 0, 0, 1],
                      [0, 1, 1, 0, 0]], 
                      dtype=np.int8)
        label_vec = np.array([1,2,3,4,5], dtype=np.int64)
        self.assertTrue(is_ddm(A, label_vec))

        A[4,4] = 1
        self.assertFalse(is_ddm(A, label_vec))

    def test_is_trivial(self):
        A = np.array([[0,1], [0,0]], dtype=np.int8)
        self.assertFalse(is_trivial(A))

        A[0, 1] = 0
        self.assertTrue(is_trivial(A))

    def test_is_connected(self):
        A = np.array([[0,1,0,0],
                      [0,0,1,0],
                      [0,0,0,1],
                      [0,0,0,0]],
                      dtype=np.int8)
        self.assertTrue(is_connected(A))
        A[1,2] = 0
        self.assertFalse(is_connected(A))

    def test_is_balanced(self):
        A = np.array([[0,1,0,0],
                      [1,0,0,0],
                      [0,0,0,1],
                      [0,0,1,0]],
                      dtype=np.int8)
        self.assertTrue(is_balanced(A))
        A[2,3] = 0
        self.assertFalse(is_balanced(A))



