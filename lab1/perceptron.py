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
        weights = np.random.rand(1,len(self.inputs[0]))
        print 'weights: ', weights
        #randomly fill weight matrix
        return weights

    def learn(self, weights, outputs, targets):
        for weights_i in weights:
            pass
            #do weights_i -= learningRate * (output - target) * input
            #for each row in weights?
        print 'Do some learning here (adjust weights)'
        return weights

    def recall(self, weights):
        outputs = []
        for inputRow in self.inputs:
            outputs.extend(list(np.dot(weights, np.transpose(inputRow))))
        outputs = map(int, map(np.sign, outputs))
        print 'recall outputs: ', outputs
        return outputs
    
    def train(self):
        #runs algorithm
        weights = self.initialize(len(self.inputs))
        #recall and learn will loop for some iterations
        #or until fully learned
        self.recall(weights)
        #self.learn(weights, ... more here to figure out)