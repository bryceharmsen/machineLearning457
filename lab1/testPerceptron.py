import unittest
from perceptron import Perceptron
import numpy as np

class PerceptronTests(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        inputs = [  [0,1,0,0,1,0,0,1,0], \
                    [1,0,0,1,0,0,1,1,1], \
                    [1,0,0,1,0,0,1,0,0], \
                    [0,0,1,0,0,1,0,0,1]]
        targets = [['i'],['l'],['i'], ['i']]
        learningRate = 0.1
        maxIterations = 1
        trainingPercentage = 0.5
        folds = 2
        self.percepter = Perceptron(inputs,targets,learningRate,maxIterations, trainingPercentage, folds)
        self.rows = len(inputs)
        self.cols = len(inputs[0])

    def test_column(self):
        matrix = [[0,1,2],[3,4,5],[6,7,8],[9,10,11]]
        self.assertEqual(self.percepter.column(matrix,0), [0,3,6,9])
        self.assertEqual(self.percepter.column(matrix,1), [1,4,7,10])
        self.assertEqual(self.percepter.column(matrix,2), [2,5,8,11])

    def test_initialize(self):
        weights = self.percepter.initialize(self.cols)
        self.assertEqual(len(weights), self.cols)
    
    def test_learn(self):
        targets = [1,-1,1,1] #target values for outputs
        outputs = [1,-1,1,1] #all correct outputs
        weights = self.percepter.initialize(self.cols + 1)
        newWeights = self.percepter.learn(weights, outputs, targets)
        self.assertListEqual(list(weights),list(newWeights))

    def test_recall(self):
        #NEED TO WORK ON THIS TEST MORE
        weights = np.ones(self.cols + 1, dtype=int)
        outputs = self.percepter.recall(weights)
        expectedOutputs = [np.sum(inputRow) for inputRow in self.percepter.inputs]
        print(weights, outputs, expectedOutputs)
        self.assertListEqual(outputs, expectedOutputs)

    def test_categorize(self):
        targets = ['a', 'a', 'b', 'b', 'a', 'b']
        expectedResult = [1, 1, -1, -1, 1, -1]
        result = self.percepter.categorize(targets)
        self.assertListEqual(result, expectedResult)

if __name__ == "__main__":
    unittest.main()