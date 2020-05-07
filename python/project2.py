import math
import random
from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import shutil
import util
from mlp import MultiLayerPerceptron
from mlpBookVersion import mlp

class Objective(object):
    def __init__(self, xDomain, yDomain):
        self.inputDim = 2
        self.outputDim = 1
        self.xDomain = xDomain
        self.yDomain = yDomain

    def calculate(self, x, y):
        return np.sin(math.pi * 10 * x + 10/(1 + y**2)) \
               + np.log(x**2 + y**2)

    def getSampleInputs(self, numSamples):
        return [[random.uniform(self.xDomain[0], self.xDomain[1]), \
                 random.uniform(self.yDomain[0], self.yDomain[1])] for j in range(numSamples)]
    
    def getSamples(self, numSamples):
        sampleInputs = self.getSampleInputs(numSamples)
        return [sample + [self.calculate(sample[0], sample[1])] for sample in sampleInputs]

#should the objective function be passed
#to the mlp as a param in the constructor?
#is that general enough?

def plotActual(xDomain, yDomain, objectiveFunc, savePath = '.'):
    figure = plt.figure()
    axis = figure.gca(projection='3d')

    x = np.arange(xDomain[0], xDomain[1], 0.5)
    y = np.arange(yDomain[0], yDomain[1], 0.5)
    x, y = np.meshgrid(x, y)
    z = objectiveFunc(x, y)

    surface = axis.plot_surface(x, y, z, cmap=cm.jet,
                                linewidth=0, antialiased=False)

    figure.colorbar(surface, shrink=0.5, aspect=5,)
    plt.savefig(f'{savePath}/objectivePlot.png')
    plt.show(block=False)
    plt.pause(2)
    plt.close()

def runMyMLP(params, inputs, objective):
    percepter = MultiLayerPerceptron(params, inputs)
    percepter.train(objective.outputDim)

def runBookMLP(params, samples, objective):
    print(samples)
    inputs = [row[:2] for row in samples]
    targets = [row[2:] for row in samples]
    percepter = mlp(inputs, targets, 2)
    percepter.mlptrain(inputs, targets, params['learningRate'], params['maxIterations'])

def generateARFF(fileName, samples):
    #open file for writing
    fullDestFilePath = f'./project2/data/{fileName}.arff'
    shutil.copy2('./project2/starter.arff', fullDestFilePath)
    with open(fullDestFilePath, 'a') as arff:
        for sample in samples:
            arff.write(f'{sample[0]},{sample[1]},{sample[2]}\n')
    #write general information (attributes etc.)
    #write sample data

if __name__ == "__main__":
    random.seed(datetime.now())
    params = util.getParams('./project2/params/params.yaml')
    print(params)
    xDomain = [1, 100]
    yDomain = [1, 100]
    objective = Objective(xDomain, yDomain)
    plotActual(xDomain, yDomain, objective.calculate, params['resultsPath'])
    numTrainingSamples = int(params['numSamples'] * params['trainingPercentage'])
    numTestingSamples = params['numSamples'] - numTrainingSamples
    inputs = objective.getSampleInputs(numTrainingSamples) #get random (x,y) coords from input domain (how many? build training/testing sets)
                                                                #split these up into training and testing inputs
    trainingSamples = objective.getSamples(numTrainingSamples)
    runMyMLP(params, inputs, objective)
    runBookMLP(params, trainingSamples, objective)
    generateARFF('samples', objective.getSamples(params['numSamples']))