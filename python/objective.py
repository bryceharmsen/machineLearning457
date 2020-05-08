import math
import numpy as np
import random
from datetime import datetime
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
        random.seed(datetime.now())
        x = [random.uniform(self.xDomain[0], self.xDomain[1]) for i in range(numSamples)]
        random.seed(datetime.now())
        y = [random.uniform(self.yDomain[0], self.yDomain[1]) for i in range(numSamples)]
        samples = [[x[i], y[i]] for i in range(numSamples)]
        return samples
    
    def getSamples(self, numSamples):
        sampleInputs = self.getSampleInputs(numSamples)
        return [sample + [self.calculate(sample[0], sample[1])] for sample in sampleInputs]