import numpy as np

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
        return weights

    def learn(self, weights, outputs, targets):
        for i in range(0, len(weights)):
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
        while (self.maxIterations > 0 and np.sum(np.subtract(outputs, self.targets)) != 0):
            print 'targets: ', self.targets
            print 'outputs: ', outputs
            weights = self.initialize(len(self.inputs), len(self.inputs[0]))
            #recall and learn will loop for some iterations
            #or until fully learned
            outputs = self.recall(weights)
            self.learn(weights, outputs, self.targets)
            self.maxIterations -= 1
        return weights, outputs