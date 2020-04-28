import numpy as np
import copy

class Perceptron(object):
    def __init__(self, inputs, targets, learningRate, maxIterations):
        self.inputs = [row + [-1] for row in inputs]
        self.targets = targets
        self.learningRate = learningRate
        self.maxIterations = maxIterations

    def column(self, array, colIdx):
        return [row[colIdx] for row in array]

    def initialize(self, numInputs, inputDimension):
        weights = np.random.rand(numInputs, inputDimension)
        weights = [[w /2 for w in row] for row in weights]
        return weights

    def learn(self, weights, outputs, targets):
        for i in range(0, len(weights)):
            if i > 0:
                weights[i] = copy.deepcopy(weights[i - 1])
            for j in range(0, len(weights[0])):
                weights[i][j] -= self.learningRate * (outputs[i] - targets[i]) * self.inputs[i][j]
        return weights

    def recall(self, weights):
        inputs_T = np.transpose(self.inputs)
        outputs = [np.dot(weights[i], self.column(inputs_T,i)) for i in range(0, len(weights))]
        outputs = map(int, map(np.sign, outputs))
        return outputs
    
    def categorize(self, targets):
        categories = [-1, 1]
        categorizedTarget = {}
        for i in range(0, len(targets)):
            if not categorizedTarget.has_key(targets[i]):
                categorizedTarget[targets[i]] = categories.pop()
            targets[i] = categorizedTarget.get(targets[i])
        return targets
    
    def train(self):
        #runs algorithm
        outputs = self.recall(self.initialize(len(self.inputs), len(self.inputs[0])))
        self.categorize(self.targets)
        iteration = 0
        weights = self.initialize(len(self.inputs), len(self.inputs[0]))
        while (iteration < self.maxIterations and np.sum(np.subtract(outputs, self.targets)) != 0):
            print 'iteration ', iteration
            print 'targets: ', self.targets
            print 'outputs: ', outputs
            #recall and learn will loop for some iterations
            #or until fully learned
            outputs = self.recall(weights)
            weights = self.learn(weights, outputs, self.targets)
            iteration += 1
        if iteration == self.maxIterations:
            print 'Exit cause: maximum iterations reached'
        elif np.sum(np.subtract(outputs, self.targets)) != 0:
            print 'Exit cause: outputs reached targets'
        else:
            print 'Exit cause: error'
        return weights, outputs