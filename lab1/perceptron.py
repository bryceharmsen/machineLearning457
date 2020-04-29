import numpy as np
import copy

class Perceptron(object):
    def __init__(self, inputs, targets, learningRate, maxIterations):
        self.inputs = [row + [-1] for row in inputs]
        self.targets = targets
        self.learningRate = learningRate
        self.maxIterations = maxIterations
        self.categorizedTarget = {}

    def column(self, array, colIdx):
        return [row[colIdx] for row in array]

    def initialize(self, numInputs, inputDimension):
        weights = np.random.rand(numInputs, inputDimension)
        weights = [[w /2 for w in row] for row in weights]
        return weights

    def learn(self, weights, outputs, targets):
        for i in range(len(weights)):
            if i > 0:
                weights[i] = copy.deepcopy(weights[i - 1])
            for j in range(len(weights[0])):
                weights[i][j] -= self.learningRate * (outputs[i] - targets[i]) * self.inputs[i][j]
        return weights

    def recall(self, weights):
        inputs_T = np.transpose(self.inputs)
        outputs = [np.dot(weights[i], self.column(inputs_T,i)) for i in range(len(weights))]
        outputs = list(map(int, map(np.sign, outputs)))
        return outputs
    
    def categorize(self, targets):
        newTargets = []
        categories = [-1, 1]
        for i in range(len(targets)):
            if not self.categorizedTarget.get(targets[i]):
                self.categorizedTarget[targets[i]] = categories.pop()
            newTargets.append(self.categorizedTarget.get(targets[i]))
        return newTargets
    
    def contextualize(self, outputs):
        contextualizedOutput = {}
        for key, value in self.categorizedTarget.items():
            if value in contextualizedOutput:
                contextualizedOutput[value].append(key)
            else:
                contextualizedOutput[value] = [key]
        return [contextualizedOutput.get(output)[0] for output in outputs]
    
    def train(self, inputs, targets):
        """Trains the weights using inputs and targets provided in the constructor"""
        targets = self.categorize(targets)
        weights = self.initialize(len(inputs), len(inputs[0]))
        outputs = self.recall(weights)
        iteration = 0
        lowestErrorCase = {'outputs': outputs, 'weights': weights}
        minError = np.sum(np.subtract(outputs, targets))
        error = minError
        while (iteration < self.maxIterations and error > 0):
            outputs = self.recall(weights)
            weights = self.learn(weights, outputs, targets)
            error = abs(np.sum(np.subtract(outputs, targets)))
            if error < minError:
                lowestErrorCase['outputs'] = outputs
                lowestErrorCase['weights'] = weights
                minError = error
            print('iteration ', iteration)
            print('targets: ', targets)
            print('outputs: ', outputs)
            iteration += 1
        if iteration == self.maxIterations:
            print('Exit cause: maximum iterations reached')
        elif np.sum(np.subtract(outputs, targets)) == 0:
            print('Exit cause: outputs reached targets')
        else:
            print('Exit cause: unknown (this should not happen)')
        return lowestErrorCase, weights, outputs
    
    def trainOnly(self):
        return self.train(self.inputs, self.targets)
    
    def test(self):
        """Tests the trained weight matrix for accuracy"""
        pass
    
    def crossValidate(self):
        """Validation"""
        pass
    
    def assess(self, input):
        """Assesses the provided input using the trained weights"""
        pass