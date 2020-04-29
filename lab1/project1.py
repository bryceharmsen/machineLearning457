#This script uses the Perceptron object to:
# 1. get user-defined parameters
# 2. create and preprocess the inputs,
# 3. pass inputs to prepare the Perceptron
# 4. train and test the Perceptron
import csv
import yaml
from typing import List, Dict, Any
from perceptron import Perceptron

def getParams(fileName):
    with open(fileName) as file:
        return yaml.full_load(file)

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

# 1. get user-defined parameters
params = getParams('params.yaml')
# 2. create and preprocess the inputs,
inputs, targets = preprocessInputsandTargetsFrom(params['inputFile'])
# 3. pass inputs to the Perceptron for learning
percepter = Perceptron(params)
# 4. train and test the Perceptron
print(f'Training and testing based on {params["inputFile"]} data')
percepter.trainAndTest(inputs, targets)