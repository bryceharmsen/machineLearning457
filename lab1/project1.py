#This script uses the Perceptron object to:
# 1. create and preprocess the inputs,
# 2. pass inputs to the Perceptron for learning
# 3. display to the user the results
import csv
from perceptron import Perceptron

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

supervisedLists = preprocess('supervisedData.csv')
inputs = [value[1] for value in supervisedLists]
targets = [value[0] for value in supervisedLists]

# 2. pass inputs to the Perceptron
learningRate = 0.1
maxIterations = 10000
percepter = Perceptron(inputs, targets, learningRate, maxIterations)
percepter.train()
# 3. display user results
print('Provide output about perceptron learning results')