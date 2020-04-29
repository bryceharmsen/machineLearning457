#This script uses the Perceptron object to:
# 1. create and preprocess the inputs,
# 2. pass inputs to the Perceptron for learning
# 3. display to the user the results
import csv
import yaml
import numpy as np
from typing import List, Dict, Any
from perceptron import Perceptron

def getParams(fileName):
    with open(fileName) as file:
        return yaml.full_load(file)

# 1. create and preprocess inputs
def preprocessInputsandTargetsFrom(fileName):
    inputs = []
    targets = []
    with open(fileName, 'r') as csvFile:
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
percepter = Perceptron(params)
#lowestErrorCase, finalWeights, finalOutputs = percepter.train(inputs, targets)
#finalWeights, finalOutputs, errorEpochs = percepter.train(inputs, targets)
#percepter.displayEpochs(errorEpochs)
# 3. display user results
#print('lowest error case: ')
#print('\tweights: ', lowestErrorCase['weights'])
#print('\toutputs: ', lowestErrorCase['outputs'])
#print('last case: ')
#print('\tweights: ', finalWeights)
#print('\toutputs: ', finalOutputs)
#print('\toutputs in context: ', percepter.contextualize(finalOutputs))
#print('targets: ', targets)
#rawDifference = np.subtract(finalOutputs, percepter.categorize(targets))
#difference = list(map(abs, map(int, map(np.sign, list(rawDifference)))))
#print('difference: ', difference)

print(f'Training and testing based on {params["inputFile"]} data')
#percepter.crossValidate(inputs, targets)
percepter.trainAndTest(inputs, targets)