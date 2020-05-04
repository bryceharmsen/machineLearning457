import numpy as np
import matplotlib.pyplot as plt
import random
from datetime import datetime
import copy
from nn import NeuralNetwork

class SingleLayerPerceptron(NeuralNetwork):
    def __init__(self, params):
        self.maxIterations = params['maxIterations']
        self.trainingPercentage = params['trainingPercentage']
        self.categorizedTarget = dict()
        self.trainedWeights = list()
        super().__init__(params)

    def initialize(self, inputDim):
        random.seed(datetime.now())
        return [random.uniform(0.1,0.5) for i in range(inputDim)]

    def learn(self, inputs, weights, outputs, targets):
        for i in range(len(inputs)):
            for j in range(len(inputs[0])):
                weights[j] -= self.learningRate * (outputs[i] - targets[i]) * inputs[i][j]
        return weights

    def recall(self, inputs, weights):
        return list( map(lambda row: int(np.sign(np.dot(weights,row))), inputs))
    
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

    def train(self, inputs, targets):
        """Trains the weights using inputs and targets provided in the constructor"""
        print('\nTRAINING:')
        categorizedTargets = self.categorize(targets)
        weights = self.initialize(len(inputs[0]))
        outputs = self.recall(inputs, weights)
        iteration = 0
        error = self.calculateError(outputs, categorizedTargets)*100
        errorEpochs = [error]
        while (iteration < self.maxIterations and error > 0):
            outputs = self.recall(inputs, weights)
            weights = self.learn(inputs, weights, outputs, categorizedTargets)
            error = self.calculateError(outputs, categorizedTargets)*100
            errorEpochs.append(error)
            print(f'iteration {iteration}\ntargets: {categorizedTargets}\noutputs: {outputs}')
            print(f'accuracy: {int(self.calcuateAccuracy(outputs, targets) * 100)}%\n')
            iteration += 1
        print('Exit cause:')
        if iteration == self.maxIterations:
            print('\tmaximum iterations reached')
        elif self.calculateError(outputs, categorizedTargets) == 0:
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
        trainingInputs, testInputs = self.appendBiasNodeTo(trainingInputs), self.appendBiasNodeTo(testInputs)
        weights, outputs, errorEpochs = self.train(trainingInputs, trainingTargets)
        print(f'\nFinal training state: \
                \n\tTraining targets: {trainingTargets} \
                \n\tTraining outputs: {self.contextualize(outputs)}')
        self.displayEpochs(errorEpochs)
        self.test(testInputs, weights, testTargets)
    
    def displayEpochs(self, errorEpochs):
        super().displayEpochs(errorEpochs, './project1/results')
