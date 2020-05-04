import unittest
from mlp import MultiLayerPerceptron
import numpy as np
import util
import copy

class PerceptronTests(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.params = {'neuronsByLayer': [2],     \
                       'learningRate': 0.2,       \
                       'numSamples': 4,           \
                       'trainingPercentage': 1.0, \
                       'beta': 3.0}
        self.inputs = [[0,0], [0,1], [1,0], [1,1]]
        self.biasedInputs = [[0,0,-1], [0,1,-1], [1,0,-1], [1,1,-1]]
        self.targets = [[0],[1],[1], [0]]
        self.weights =[[[1,1],[1,1], [0.5,1]],[[1],[-1],[0.5]]]
        (copyParams, copyInputs) = copy.deepcopy((self.params, self.inputs))
        self.percepter = MultiLayerPerceptron(copyParams, copyInputs)

    def testConstructor(self):
        (copyParams, copyInputs) = copy.deepcopy((self.params, self.inputs))
        testPercepter = MultiLayerPerceptron(copyParams, copyInputs)
        expectedParams = list(map(lambda x:x+1, self.params['neuronsByLayer']))
        self.assertListEqual(expectedParams, testPercepter.params['neuronsByLayer'])
        self.assertListEqual(self.biasedInputs, testPercepter.inputs)

    def testInitializeWeights(self):
        weights = self.percepter.initializeWeights(len(self.biasedInputs[0]), self.percepter.params['neuronsByLayer'], 1)
        #count number of hidden layers + output layer
        self.assertEqual(len(weights), len(self.weights))
        for i in range(len(self.weights)):
            self.assertEqual(len(weights[i]), len(self.weights[i]))
            for j in range(len(self.weights[i])):
                self.assertEqual(len(weights[i][j]), len(self.weights[i][j]))



if __name__ == "__main__":
    unittest.main()