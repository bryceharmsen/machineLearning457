#This script uses the Perceptron object to:
# 1. create and preprocess the inputs,
# 2. pass inputs to the Perceptron for learning
# 3. display to the user the results
import csv
import yaml
from perceptron import Perceptron

def getParams(fileName):
    with open(fileName) as file:
        return yaml.load(file, Loader=yaml.FullLoader)

# 1. create and preprocess inputs
def preprocess(fileName):
    lists = []
    with open(fileName, 'rb') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        currList = []
        for row in reader:
            if len(row) == 1:
                target = row[0]
                lists.append((target, currList))
                currList = []
            else:
                currList.extend(list(map(int, row)))
    return lists

def buildConfusionMatrix(outputs, targets):
    truePos = 0
    falsePos = 0
    trueNeg = 0
    falseNeg = 0

params = getParams('params.yaml')
supervisedLists = preprocess(params['inputFile'])
inputs = [value[1] for value in supervisedLists]
targets = [value[0] for value in supervisedLists]

# 2. pass inputs to the Perceptron
percepter = Perceptron(inputs, targets, params['learningRate'], params['maxIterations'])
lowestErrorCase, weights, outputs = percepter.train()
# 3. display user results
print 'lowest error case: '
#print '\tweights: ', lowestErrorCase['weights']
print '\toutputs: ', lowestErrorCase['outputs']
print 'last case: '
#print '\tweights: ', weights
print '\toutputs: ', outputs
print 'Provide output about perceptron learning results'