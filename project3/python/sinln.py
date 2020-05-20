import sys
import math
import numpy as np
import random
from datetime import datetime
import copy
from types import SimpleNamespace
from operator import attrgetter
import plotter
import util
from ga import GA, Chrom, ChromList

class SinLn(GA):
    def __init__(self, generations, populationSize, mutationRate, xDomain, yDomain, **kwargs):
        self.xDomain = xDomain
        self.yDomain = yDomain
        random.seed(datetime.now())
        np.random.seed(int(datetime.timestamp(datetime.now())))
        super(SinLn, self).__init__(generations, populationSize, mutationRate)
    
    def f(self, x, y):
        return np.sin(math.pi * 10 * x + 10/(1 + y**2)) \
               + np.log(x**2 + y**2)

    def createChromosomes(self) -> ChromList:
        return [Chrom([np.random.uniform(*self.xDomain), np.random.uniform(*self.yDomain)], 0) for _ in range(self.populationSize)]

    def select(self, chromosomes: ChromList) -> ChromList:
        #which form of select? rank (no), roulette, tournament?
        
        #Roulette wheel selection (proportionate)
        #get sum of fitnesses
        chromosomes = copy.deepcopy(chromosomes)
        fitnessesSum = self.getFitnessesSum(chromosomes)
        #sort descending the chroms
        chromosomes = self.sortChromosomes(chromosomes)
        #initiate parents list
        parents = []
        origNumChroms = len(chromosomes)
        #while selection list is less than half
        #the orig. size of the pop.
        while len(parents) < origNumChroms / 2:
            #get rand between 0 and sum
            target = random.uniform(0, fitnessesSum)
            partialSum = 0
            selectedParent = chromosomes[0]
            selectedIdx = 0
            #while partial sum < rand
            for i, chrom in enumerate(chromosomes):
                #add next fitness value to partial sum
                partialSum += chrom.fitness
                #selected parent set to this chrom
                if partialSum >= target:
                    selectedParent = chrom
                    selectedIdx = i
                    break
            #append selected parent to parents list
            parents.append(selectedParent)
            #remove selected parent from chromosomes
            chromosomes.pop(selectedIdx)
        #return parents list
        return parents

    def getFitnessesSum(self, chromosomes: ChromList) -> float:
        return sum(chrom.fitness for chrom in chromosomes)

    def crossover(self, parents: ChromList) -> ChromList:
        #let's stick with single point crossover for now
        #should it just be x from one, y from the other? or
        #should it be parts of the bit string of x and/or y from
        #one and the other parts of bit string from the rest?

        #BASIC
        #shuffle parents
        parents = copy.deepcopy(parents)
        random.shuffle(parents)
        #create offspring list
        offspring = []
        #for each pair of even and odd parents
        if len(parents) % 2 == 1:
            parents.append(parents[int(np.random.uniform(0, len(parents)))])
        for i in range(1, len(parents)):
            if i % 2 == 1:
                parentA = parents[i - 1]
                parentB = parents[i]
                #randomly decide where to cross over
                crossoverIdx = int(math.floor(np.random.uniform(0, 2)))
                #create two offspring based on crossover point
                currOffspring = [
                    Chrom(parentA.alleles[:crossoverIdx] + parentB.alleles[crossoverIdx:], 0),
                    Chrom(parentB.alleles[:crossoverIdx] + parentA.alleles[crossoverIdx:], 0)
                ]
                currOffspring = self.setFitnesses(currOffspring)
                #append new offspring to offspring list
                offspring.extend(currOffspring)
        #concatenate parents and offspring lists
        return offspring

    def mutate(self, offspring: ChromList) -> ChromList:
        #perform bit flip on float?
        #if uniform random in [0, 1) is between 0 and mutationRate
            #mutate some portion (small portion, like a bit or x or y val)
            #of the current offspring
            #mutation idx from uniform random as well
        #BASIC
        for chrom in offspring:
            randRate = random.uniform(0, 1)
            if randRate < self.mutationRate:
                idx = np.random.randint(0, 2)
                if idx == 0:
                    chrom.alleles[idx] = random.uniform(*self.xDomain)
                else:
                    chrom.alleles[idx] = random.uniform(*self.yDomain)
        return offspring

    def setFitnesses(self, chromosomes: ChromList) -> ChromList:
        for chrom in chromosomes:
            chrom.fitness = self.f(*chrom.alleles)
        return chromosomes

    def sortChromosomes(self, chromosomes: ChromList, descending=True) -> ChromList:
        chromosomes.sort(key=attrgetter('fitness'), reverse=descending)
        return chromosomes

    def getMostFitChromosome(self, chromosomes: ChromList) -> Chrom:
        mostFitChrom = chromosomes[0]
        for chrom in chromosomes:
            if chrom.fitness > mostFitChrom.fitness:
                mostFitChrom = copy.deepcopy(chrom)
        return mostFitChrom
        
if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print(f'Proper use:\n\tpython3 {sys.argv[0]} PARAM_FILENAME.yaml')
    params = util.getParams(sys.argv[1])
    ga = SinLn(**params)
    plotter.plot3d(ga.xDomain, ga.yDomain, ga.f)
    bestChromsByGen = ga.run()
    plotter.plot2dTimeSeries(
        [chrom.fitness for chrom in bestChromsByGen],
        'Best Chromosome By Generation',
        'generation',
        'z-value'
    )
    plotter.plot2dScatter(
        [chrom.alleles[0] for chrom in bestChromsByGen],
        [chrom.alleles[1] for chrom in bestChromsByGen]
    )
    print(f'best chromosomes: {[chrom.alleles for chrom in bestChromsByGen]}')