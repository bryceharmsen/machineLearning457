import numpy as np
import matplotlib.pyplot as plt
import copy

class Perceptron(object):
    def __init__(self, params):
        self.learningRate = params['learningRate']
        self.maxIterations = params['maxIterations']
        self.trainingPercentage = params['trainingPercentage']
        self.categorizedTarget = dict()
        self.trainedWeights = list()

    def column(self, array, colIdx):
        return [row[colIdx] for row in array]
    
    def appendExtraNodeTo(self, inputs):
        return [row + [-1] for row in inputs]

    def initialize(self, inputDim):
        weights = np.random.rand(inputDim)
        weights = [w * 0.4 + 0.1 for w in weights]
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
    
    def getError(self, outputs, targets):
        return np.sum([abs(diff) for diff in np.subtract(outputs, targets)])

    def train(self, inputs, targets):
        """Trains the weights using inputs and targets provided in the constructor"""
        print('TRAINING:')
        targets = self.categorize(targets)
        weights = self.initialize(len(inputs[0]))
        outputs = self.recall(inputs, weights)
        iteration = 0
        #lowestErrorCase = {'outputs': outputs, 'weights': weights}
        #minError = np.sum(np.subtract(outputs, targets))
        #error = minError
        error = self.getError(outputs, targets)
        errorEpochs = [error]
        while (iteration < self.maxIterations and error > 0):
            outputs = self.recall(inputs, weights)
            weights = self.learn(inputs, weights, outputs, targets)
            error = self.getError(outputs, targets)
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
        elif self.getError(outputs, targets) == 0:
            print('Exit cause: outputs matched targets')
        else:
            print('Exit cause: unknown (this should not happen)')
        #return lowestErrorCase, weights, outputs
        return weights, outputs, errorEpochs
    
    def test(self, inputs, weights, targets):
        """Tests the trained weight matrix for accuracy"""
        print(f'TESTING:\n\tinputs: {inputs}\n\ttargets: {targets}')
        outputs = self.recall(inputs, weights)
        contextualizedOutputs = self.contextualize(outputs)
        diffs = np.subtract(outputs, self.categorize(targets))
        numCorrect = 0
        for diff in diffs:
            if diff == 0:
                numCorrect += 1
        accuracy = numCorrect / len(targets)
        print(f'\toutputs: {contextualizedOutputs}\n\taccuracy: {accuracy * 100}%')
    
    #def splitIntoChunks(self, inputs, targets):
    #    chunks = [[] for i in range(self.folds)]
    #    for i in range(len(targets)):
    #       chunks[i % len(chunks)].append((inputs[i], targets[i]))
    #    return chunks
    
    def split(self, inputs, targets):
        trainingInputs = inputs[::2]
        testInputs = inputs[1::2]
        trainingTargets = targets[::2]
        testTargets = targets[1::2]
        return trainingInputs, trainingTargets, testInputs, testTargets


    def trainAndTest(self, inputs, targets):
        trainingInputs, trainingTargets, testInputs, testTargets = self.split(inputs, targets)
        weights, outputs, errorEpochs = self.train(trainingInputs, trainingTargets)
        print(f'Training targets: {trainingTargets}\nTraining outputs: {self.contextualize(outputs)}')
        self.displayEpochs(errorEpochs)
        self.test(testInputs, weights, testTargets)

    #def crossValidate(self, inputs, targets):
    #    """Validation"""
    #    self.appendExtraNodeTo(inputs)
    #   chunks = self.splitIntoChunks(inputs, targets)   
    #    for i in range(self.folds):
    #        #group test and train chunks
    #        testChunk = chunks.pop()
    #        validationChunk = chunks.pop()
    #       trainingChunks = chunks
    #       #train
    #       flattenedTrainingChunk = sum(trainingChunks, [])
    #       #lowestErrorCase, weights, outputs = self.train([x[0] for x in flattenedChunk], [x[1] for x in flattenedChunk])
    #        trainingInputs = [x[0] for x in flattenedTrainingChunk]
    #       trainingTargets = [x[1] for x in flattenedTrainingChunk]
    #       weights, outputs, errorEpochs = self.train(trainingInputs, trainingTargets)
    #       self.displayEpochs(errorEpochs)
    #        #test
    #        testInputs = [x[0] for x in testChunk]
    #        testTargets = [x[1] for x in testChunk]
    #        self.test(testInputs, weights, testTargets)
    #        #rotate and re-assemble chunks
    #        trainingChunks.append(validationChunk)
    #        chunks = [testChunk]
    #        chunks.extend(trainingChunks)
    
    def displayEpochs(self, errorEpochs):
        plt.plot(errorEpochs)
        plt.ylabel('error')
        plt.xlabel('epoch')
        plt.show()