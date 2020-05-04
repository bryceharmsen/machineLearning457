import numpy as np
import math
import random
from datetime import datetime
from nn import NeuralNetwork

class MultiLayerPerceptron(NeuralNetwork):
    def __init__(self, params, inputs):
        super().__init__(params)
        random.seed(datetime.now())
        self.beta = params['beta']
        self.params, self.inputs = self.imposeBias(params, inputs)

    def imposeBias(self, params, inputs):
        """Add bias nodes and alter network dimensions"""
        params['neuronsByLayer'] = [n + 1 for n in params['neuronsByLayer']]
        return params, self.appendBiasNodeTo(inputs)

    def initializeWeights(self, inputDim, neuronsByLayer, outputDim):
        weightDims = [inputDim] + neuronsByLayer + [outputDim]
        weights = []
        randSign = lambda x : x if random.random() < 0.5 else -x
        for i in range(len(weightDims) - 1):
            cols = weightDims[i+1] if i+1 == len(weightDims)-1 else weightDims[i+1] - 1
            weights.append([[randSign(random.uniform(0.1,0.5)) for j in range(cols)] for k in range(weightDims[i])])
        return weights
    
    def activate(self, funcName):
        activationFuncs = {
            'linear': lambda x : x,
            #'logarithmic': lambda x : 1 / (1 + math.exp(-1 * self.beta * x)),
            'sigmoid': np.tanh,
        }
        return activationFuncs.get(funcName)

    def activateNeuron(self, inputs, weights):
        return self.activate('sigmoid')()

    def activateOutput(self, inputs, weights):
        return []
    
    def recall(self, inputs, weights):
        outputs = []
        for i, wSet in enumerate(weights):
            if i < len(weights) - 1:
                inputs = self.activateNeuron(inputs, wSet)
            else:
                outputs = self.activateOutput(inputs, wSet)
        return outputs

    def updateWeights(self):
        return []

    def isLearning(self):
        pass

    def train(self, outputDim):
        weights = self.initializeWeights(len(self.inputs[0]),self.params['neuronsByLayer'], outputDim)
        while self.isLearning():
            outputs = self.recall(self.inputs, weights)
            weights = self.updateWeights()
        #while learning is happening
            #FORWARDS PHASE
            ##for each hidden layer
                #compute activation of each neuron
                ##h_neuron = dot product inputs by weights
                ##activation_neuron = g_neuron(h_neuron)
            ##output layer
             #compute activation of output
             ##h_out = dot product of neurons by weights
             ##activation_out = g_out(h_out)
            #BACKWARDS PHASE
            ##compute error at output
             #delta_out = derivative_g_out(y, t)
            ##(reversed)for each hidden layer
                #compute error
                ##delta_neuron = derivative_g_neuron(activation) * dot product weights by delta_out
            ##update output layer weights
             #weights -= learning_rate * delta_out * activation_neuron
            #(reversed)for each hidden layer
                #update hidden layer weights
                ##weights -= learning_rate * delta_neuron * input
        return weights

    def test(self, weights):
        #for each test input
            #output = recall using input and weights
            #error = output - target
            #either add to error or append to list of errors
        pass
