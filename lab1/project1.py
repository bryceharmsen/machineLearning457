#This script uses the Perceptron object to:
# 1. create and preprocess the inputs,
# 2. pass inputs to the Perceptron for learning
# 3. display to the user the results
import csv
import yaml
import numpy as np
from perceptron import Perceptron

def getParams(fileName):
    with open(fileName) as file:
        return yaml.load(file, Loader=yaml.FullLoader)

# 1. create and preprocess inputs
def preprocessInputsandTargetsFrom(fileName):
    inputs = []
    targets = []
    with open(fileName, 'rb') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        currInputsRow = []
        for row in reader:
            if len(row) == 1:
                targets.append(row[0])
                inputs.append(currInputsRow)
                currInputsRow = []
            else:
                currInputsRow.extend(list(map(int, row)))
    return inputs, targets

def buildConfusionMatrix(outputs, targets):
    truePos = 0
    falsePos = 0
    trueNeg = 0
    falseNeg = 0

params = getParams('params.yaml')
inputs, targets = preprocessInputsandTargetsFrom(params['inputFile'])

# 2. pass inputs to the Perceptron
percepter = Perceptron(inputs, targets, params['learningRate'], params['maxIterations'])
lowestErrorCase, finalWeights, finalOutputs = percepter.train()
# 3. display user results
print 'lowest error case: '
#print '\tweights: ', lowestErrorCase['weights']
print '\toutputs: ', lowestErrorCase['outputs']
print 'last case: '
#print '\tweights: ', finalWeights
print '\toutputs: ', finalOutputs
print '\toutputs in context: ', percepter.contextualize(finalOutputs)
print 'targets: ', targets
rawDifference = np.subtract(finalOutputs, percepter.categorize(targets))
difference = map(abs, map(int, map(np.sign, list(rawDifference))))
print 'difference: ', difference