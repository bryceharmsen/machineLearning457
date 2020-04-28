import unittest
from perceptron import Perceptron

class PerceptronTests(unittest.TestCase):

    def test_first(self):
        result = 0
        self.assertEqual(result, 0)

    def test_second(self):
        result = 0
        self.assertEqual(result, 1)

if __name__ == "__main__":
    unittest.main()