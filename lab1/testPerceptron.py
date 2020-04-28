import unittest
from perceptron import Perceptron

class PerceptronTests(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.percepter = Perceptron([[0,1,0,0,1,0,0,1,0]],[['i']],0.1,1)

    def test_first(self):
        result = 0
        self.assertEqual(result, 0)

    def test_column(self):
        matrix = [[0,1,2],[3,4,5],[6,7,8],[9,10,11]]
        self.assertEqual(self.percepter.column(matrix,0), [0,3,6,9])
        self.assertEqual(self.percepter.column(matrix,1), [1,4,7,10])
        self.assertEqual(self.percepter.column(matrix,2), [2,5,8,11])

if __name__ == "__main__":
    unittest.main()