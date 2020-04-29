import numpy as np
import copy

class Perceptron(object):
    def __init__(self, params):
        self.learningRate = params['learningRate']
        self.maxIterations = params['maxIterations']
        self.trainingPercentage = params['trainingPercentage']
        self.folds = params['folds']
        self.categorizedTarget = dict()
        self.trainedWeights = list()

    def column(self, array, colIdx):
        return [row[colIdx] for row in array]
    
    def appendExtraNodeTo(self, inputs):
        return [row + [-1] for row in inputs]

    def initialize(self, inputDim):
        weights = np.random.rand(inputDim)
        weights = [w * 0.4 + 0.1 for w in weights]
        print(weights)
        return weights

    def learn(self, inputs, weights, outputs, targets):
        for i in range(len(inputs)):
            for j in range(len(inputs[0])):
                weights[j] -= self.learningRate * (outputs[i] - targets[i]) * inputs[i][j]
        return weights

    def recall(self, inputs, weights):
        inputs_T = np.transpose(inputs)
        outputs = [np.dot(weights, self.column(inputs_T,i)) for i in range(len(inputs_T[0]))]
        outputs = list(map(int, map(np.sign, outputs)))
        return outputs
    
    def categorize(self, targets):
        newTargets = list()
        categories = [-1, 1]
        for i in range(len(targets)):
            if not self.categorizedTarget.get(targets[i]):
                self.categorizedTarget[targets[i]] = categories.pop()
            newTargets.append(self.categorizedTarget.get(targets[i]))
        return newTargets
    
    def contextualize(self, outputs):
        contextualizedOutput = dict()
        for key, value in self.categorizedTarget.items():
            if value in contextualizedOutput:
                contextualizedOutput[value].append(key)
            else:
                contextualizedOutput[value] = [key]
        return [contextualizedOutput.get(output)[0] for output in outputs]
    
    def train(self, inputs, targets):
        """Trains the weights using inputs and targets provided in the constructor"""
        targets = self.categorize(targets)
        weights = self.initialize(len(inputs[0]))
        outputs = self.recall(inputs, weights)
        iteration = 0
        #lowestErrorCase = {'outputs': outputs, 'weights': weights}
        #minError = np.sum(np.subtract(outputs, targets))
        #error = minError
        error = np.sum(np.subtract(outputs, targets))
        errorEpochs = [error]
        while (iteration < self.maxIterations and error > 0):
            outputs = self.recall(inputs, weights)
            weights = self.learn(inputs, weights, outputs, targets)
            error = abs(np.sum(np.subtract(outputs, targets)))
            errorEpochs.append(error)
            #if error < minError:
            #    lowestErrorCase['outputs'] = outputs
            #    lowestErrorCase['weights'] = weights
            #    minError = error
            print('iteration ', iteration)
            print('targets: ', targets)
            print('outputs: ', outputs)
            iteration += 1
        if iteration == self.maxIterations:
            print('Exit cause: maximum iterations reached')
        elif np.sum(np.subtract(outputs, targets)) == 0:
            print('Exit cause: outputs matched targets')
        else:
            print('Exit cause: unknown (this should not happen)')
        #return lowestErrorCase, weights, outputs
        return weights, outputs, errorEpochs
    
    def test(self, inputs):
        """Tests the trained weight matrix for accuracy"""
        for input in inputs:
            pass
        pass

    def validate(self):
        pass
    
    def splitIntoChunks(self, inputs, targets):
        chunks = [[] for i in range(self.folds)]
        for i in range(len(targets)):
            chunks[i % len(chunks)].append((inputs[i], targets[i]))
        return chunks

    def crossValidate(self, inputs, targets):
        """Validation"""
        self.appendExtraNodeTo(inputs)
        chunks = self.splitIntoChunks(inputs, targets)   
        for i in range(self.folds):
            testChunk = chunks.pop()
            validationChunk = chunks.pop()
            trainingChunks = chunks
            #train
            flattenedChunk = sum(trainingChunks, [])
            #lowestErrorCase, weights, outputs = self.train([x[0] for x in flattenedChunk], [x[1] for x in flattenedChunk])
            weights, outputs, errorEpochs = self.train([x[0] for x in flattenedChunk], [x[1] for x in flattenedChunk])
            #test
            self.test(testChunk)
            #validate
            self.validate()
            #rotate and re-assemble chunks
            trainingChunks.append(validationChunk)
            chunks = [testChunk]
            chunks.extend(trainingChunks)

    def assess(self, input):
        """Assesses the provided input using the trained weights"""
        pass