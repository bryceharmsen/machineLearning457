import numpy as np
import matplotlib.pyplot as plt
import copy

class Perceptron(object):
    def __init__(self, params):
        self.learningRate = params['learningRate']
        self.maxIterations = params['maxIterations']
        self.trainingPercentage = params['trainingPercentage']
        self.categorizedTarget = dict()
        self.trainedWeights = list()

    def column(self, array, colIdx):
        return [row[colIdx] for row in array]
    
    def appendExtraNodeTo(self, inputs):
        return [row + [-1] for row in inputs]

    def initialize(self, inputDim):
        weights = np.random.rand(inputDim)
        weights = [w * 0.4 + 0.1 for w in weights]
        return weights

    def learn(self, inputs, weights, outputs, targets):
        for i in range(len(inputs)):
            for j in range(len(inputs[0])):
                weights[j] -= self.learningRate * (outputs[i] - targets[i]) * inputs[i][j]
        return weights

    def recall(self, inputs, weights):
        inputs_T = np.transpose(inputs)
        outputs = [np.dot(weights, self.column(inputs_T,i)) for i in range(len(inputs_T[0]))]
        outputs = list(map(int, map(np.sign, outputs)))
        return outputs
    
    def categorize(self, targets):
        newTargets = list()
        categories = [-1, 1]
        for i in range(len(targets)):
            if not self.categorizedTarget.get(targets[i]):
                self.categorizedTarget[targets[i]] = categories.pop()
            newTargets.append(self.categorizedTarget.get(targets[i]))
        return newTargets
    
    def contextualize(self, outputs):
        contextualizedOutput = dict()
        for key, value in self.categorizedTarget.items():
            if value in contextualizedOutput:
                contextualizedOutput[value].append(key)
            else:
                contextualizedOutput[value] = [key]
        return [contextualizedOutput.get(output)[0] for output in outputs]
    
    def getError(self, outputs, targets):
        return (1 - self.calcuateAccuracy(outputs, targets)) * 100

    def train(self, inputs, targets):
        """Trains the weights using inputs and targets provided in the constructor"""
        print('\nTRAINING:')
        categorizedTargets = self.categorize(targets)
        weights = self.initialize(len(inputs[0]))
        outputs = self.recall(inputs, weights)
        iteration = 0
        error = self.getError(outputs, categorizedTargets)
        errorEpochs = [error]
        while (iteration < self.maxIterations and error > 0):
            outputs = self.recall(inputs, weights)
            weights = self.learn(inputs, weights, outputs, categorizedTargets)
            error = self.getError(outputs, categorizedTargets)
            errorEpochs.append(error)
            print(f'iteration {iteration}\ntargets: {categorizedTargets}\noutputs: {outputs}')
            print(f'accuracy: {int(self.calcuateAccuracy(outputs, targets) * 100)}%\n')
            iteration += 1
        print('Exit cause:')
        if iteration == self.maxIterations:
            print('\tmaximum iterations reached')
        elif self.getError(outputs, categorizedTargets) == 0:
            print('\toutputs matched targets')
        else:
            print('\tunknown (this should not happen)')
        return weights, outputs, errorEpochs
    
    def calcuateAccuracy(self, outputs, targets):
        """Calculate accuracy of outputs matching targets for given samples"""
        diffs = np.subtract(outputs, self.categorize(targets))
        numCorrect = 0
        for diff in diffs:
            if diff == 0:
                numCorrect += 1
        return numCorrect / len(targets)

    def test(self, inputs, weights, targets):
        """Tests the trained weight matrix for accuracy"""
        outputs = self.recall(inputs, weights)
        accuracy = self.calcuateAccuracy(outputs, targets)
        print(f'\nTESTING:\n\ttargets: {targets} \
                \n\toutputs: {self.contextualize(outputs)} \
                \n\taccuracy: {int(accuracy * 100)}%')
    
    def split(self, inputs, targets):
        """Split data samples into training and testing sets"""
        trainingInputs = inputs[::2]
        testInputs = inputs[1::2]
        trainingTargets = targets[::2]
        testTargets = targets[1::2]
        return trainingInputs, trainingTargets, testInputs, testTargets


    def trainAndTest(self, inputs, targets):
        """Split incoming samples, then train and test sample sets"""
        trainingInputs, trainingTargets, testInputs, testTargets = self.split(inputs, targets)
        weights, outputs, errorEpochs = self.train(trainingInputs, trainingTargets)
        print(f'\nFinal training state: \
                \n\tTraining targets: {trainingTargets} \
                \n\tTraining outputs: {self.contextualize(outputs)}')
        self.displayEpochs(errorEpochs)
        self.test(testInputs, weights, testTargets)
    
    def displayEpochs(self, errorEpochs):
        """Plot error across training epochs"""
        plt.plot(errorEpochs)
        plt.ylabel('error (%)')
        plt.xlabel('epoch')
        plt.xticks(range(len(errorEpochs)))
        plt.show()