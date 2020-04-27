import numpy as np

#good functions to keep in mind:
# np.dot()
# np.sign()
# np.ones()

class Perceptron(object):
    def __init__(self, inputs, learningRate):
        self.inputs = inputs
        self.learningRate = learningRate

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