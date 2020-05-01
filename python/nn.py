import numpy as np
import matplotlib.pyplot as plt
import random
from datetime import datetime

class NeuralNetwork(object):
    def __init__(self, params):
        self.learningRate = params['learningRate']

    def column(self, array, colIdx):
        return [row[colIdx] for row in array]
    
    def appendExtraNodeTo(self, inputs):
        return [row + [-1] for row in inputs]

    def initializeWeights(self, numInputs, numNeurons):
        random.seed(datetime.now())
        #TODO: should this be numInputs x numNeurons or switched?
        return [[random.uniform(0.1,0.5) for i in range(numInputs)] for j in range(numNeurons)]

    def updateWeights(self, inputs, weights, outputs, targets, adjustmentFunc):
        for i in range(len(inputs)):
            for j in range(len(inputs[0])):
                #TODO: determine what should go to adjustmentFunc for general case
                weights[j] -= self.learningRate * adjustmentFunc(outputs, targets) * inputs[i][j]
        return weights

    def recall(self, inputs, weights):
        inputs_T = np.transpose(inputs)
        outputs = [np.dot(weights, self.column(inputs_T,i)) for i in range(len(inputs_T[0]))]
        outputs = list(map(int, map(np.sign, outputs)))
        return outputs
    
    def calcuateAccuracy(self, outputs, targets):
        """Calculate accuracy of outputs matching targets for given samples"""
        #TODO: shorten this up.
        diffs = np.subtract(outputs, targets)
        numCorrect = 0
        for diff in diffs:
            if diff == 0:
                numCorrect += 1
        return numCorrect / len(targets)

    def calculateError(self, outputs, targets):
        return (1 - self.calcuateAccuracy(outputs, targets))
    
    def displayEpochs(self, errorEpochs, savePath = '.'):
        """Plot error across training epochs"""
        plt.plot(errorEpochs)
        plt.ylabel('error (%)')
        plt.xlabel('epoch')
        plt.xticks(range(len(errorEpochs)))
        plt.savefig(f'{savePath}/errorEpochs.png')
        plt.title('Training Error by Epoch')
        plt.show(block=False)
        plt.pause(1)
        plt.close()