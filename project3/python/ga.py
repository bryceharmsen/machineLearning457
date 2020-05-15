#class imports
import numpy as np
#driver imports
import sys
import util
from sinln import Objective

class ChromRecord:
    def __init__(self, chromosome, fitness):
        self.chromosome = chromosome
        self.fitness = fitness

class GA:
    def __init__(self, params, objectiveFunc):
        self.chromosomes = params['chromosomes']
        self.generations = params['generations']
        self.mutationRate = params['mutationRate']
        self.crossoverRate = params['crossoverRate']
        self.xDomain = params['xDomain']
        self.yDomian = params['yDomain']
        self.f = objectiveFunc

    def select(self):
        pass
    
    def crossover(self):
        #for half of population to crossover
            #pair up with other half of crossover pop.
            #determine random index to perform crossover
            #generate new pop. member with crossover sections
        pass

    def mutate(self):
        #for each population member
            #based on mutation likelihood percentage (yaml)
            #if random val is between 0 and mutation constant
                #alter value
                #either += rand between 0 and maxXorY - value
                #or -= rand between 0 and minXorY - value
        pass

    def getNextGen(self, chromosomes, fitnesses):
        #select, crossover, and mutate current gen
        #select (even number of) parents based on fitness (rank, roulette, tournament)
        #crossover parents (in sets of 2)
        #mutate offspring (set mutation constant for roughly how often to mutate)
        return chromosomes, fitnesses

    def createInitGen(self):
        xChroms = np.random.uniform(self.xDomain[0], self.xDomain[1], (self.chromosomes,1))
        yChroms = np.random.uniform(self.yDomian[0], self.yDomian[1], (self.chromosomes,1))
        return np.concatenate((xChroms, yChroms), axis=1)

    def getFitness(self, chromosomes):
        return self.f(chromosomes[:,:1], chromosomes[:,1:])

    def getBest(self, chromosomes, fitnesses):
        bestFitIdx = np.argmax(fitnesses)
        return ChromRecord(chromosomes[bestFitIdx], fitnesses[bestFitIdx])

    def run(self):
        #build initial population
        chromosomes = self.createInitGen()
        fitnesses = self.getFitness(chromosomes)
        bestChrom = self.getBest(chromosomes, fitnesses)
        bestChromByGen = [bestChrom]
        #for each generation
        for _ in range(1, self.generations):
            #getNextGen
            chromosomes, fitnesses = self.getNextGen(chromosomes, fitnesses)
            #save most fit chromosome in generation
            newBestChrom = self.getBest(chromosomes, fitnesses)
            bestChromByGen.append(newBestChrom)
            #save fitness value for best chromosome
            if newBestChrom.fitness > bestChrom.fitness:
                bestChrom = newBestChrom
        #report most fit chromosome
        #report most fit for each generation

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f'Proper use:\n\tpython3 {sys.argv[0]} PARAMS_FILE_NAME')
        exit(1)
    params = util.getParams(sys.argv[1])
    objective = Objective()
    ga = GA(params, objective.f)
    ga.run()