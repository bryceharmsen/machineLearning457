#This script uses the Perceptron object to:
# 1. create and preprocess the inputs,
# 2. pass inputs to the Perceptron for learning
# 3. display to the user the results

from perceptron import Perceptron

#create and preprocess inputs
inputs = []

#pass inputs to the Perceptron
learningRate = 0.25
maxIterations = 10
percepter = Perceptron(inputs, learningRate, maxIterations)
percepter.run()
#display user results
print('Provide output about perceptron learning results')