#This script uses the Perceptron object to:
# 1. get user-defined parameters
# 2. create and preprocess the inputs,
# 3. pass inputs to prepare the Perceptron
# 4. train and test the Perceptron
import sys
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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f'Proper use of this program looks like: \
               \n\tpython3 {sys.argv[0]} params*.yaml \
               \n\nExiting gracefully...')
        sys.exit()
    # 1. get user-defined parameters
    params = getParams(sys.argv[1])
    # 2. create and preprocess the inputs,
    inputs, targets = preprocessInputsandTargetsFrom(params['inputFile'])
    print(f'Number of data samples: {len(targets):d}')
    # 3. pass inputs to the Perceptron for learning
    percepter = Perceptron(params)
    # 4. train and test the Perceptron
    print(f'Training and testing based on {params["inputFile"]} data')
    percepter.trainAndTest(inputs, targets)
