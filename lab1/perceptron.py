import numpy as np

#good functions to keep in mind:
# np.dot()
# np.sign()
# np.ones()

class Perceptron(object):
    def __init__(self, inputs, learningRate, maxIterations):
        self.inputs = inputs
        self.learningRate = learningRate
        self.maxIterations = maxIterations

    def initialize(self, numInputs):
        weights = [[]]
        #randomly fill weight matrix
        return weights

    def learn(self, weights, outputs, targets):
        for weights_i in weights:
            pass
            #do weights_i -= learningRate * (output - target) * input
            #for each row in weights?
        return weights

    def recall(self, weights):
        outputs = []
        for weights_i in weights:
            outputs.append(np.dot(weights_i, self.inputs))
        return outputs
    
    def train(self):
        #runs algorithm
        weights = self.initialize(len(self.inputs))
        #recall and learn will loop for some iterations
        #or until fully learned
        self.recall(weights)
        #self.learn(weights, ... more here to figure out)