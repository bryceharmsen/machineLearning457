import unittest
from sinln import SinLn, Chrom
from types import SimpleNamespace
from operator import attrgetter
import numpy as np
import math
import util
import copy

NUM_ALLELES = 2
OFFSPRING_MULTIPLIER = 1
VARIANCE_PERCENTAGE = 0.05

class SinLnTests(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.params = SimpleNamespace(**util.getParams('params.yaml'))
        self.ga = SinLn(**util.getParams('params.yaml'))

    def testConstructor(self):
        self.assertEqual(self.ga.generations, self.params.generations)
        self.assertEqual(self.ga.populationSize, self.params.populationSize)
        self.assertEqual(self.ga.mutationRate, self.params.mutationRate)

    def testShapeOfCreatedChromosomes(self):
        chromosomes = self.ga.createChromosomes()
        self.assertEqual(len(chromosomes), self.params.populationSize)
        self.assertEqual(len(chromosomes[0].alleles), NUM_ALLELES)
    
    def testDomainOfCreatedChromosomes(self):
        chromosomes = self.ga.createChromosomes()
        self.assertIs(
            all(
                self.params.xDomain[0] <= chrom.alleles[0] <= self.params.xDomain[1]
                and self.params.yDomain[0] <= chrom.alleles[1] <= self.params.yDomain[1]
                for chrom in chromosomes
            ), True
        )
    
    def testSetFitnesses(self):
        chromosomes = self.ga.createChromosomes()
        chromsCopy = self.ga.setFitnesses(copy.deepcopy(chromosomes))
        for chrom in chromosomes:
            chrom.fitness = self.ga.f(chrom.alleles[0], chrom.alleles[1])
        self.assertIs(
            all(
                chromsCopy[i].fitness == chromosomes[i].fitness
                for i in range(len(chromosomes)
                )
            ), True
        )
    
    def testGetMostFitChromosome(self):
        chromosomes = self.ga.createChromosomes()
        for chrom in chromosomes:
            chrom.fitness = self.ga.f(chrom.alleles[0], chrom.alleles[1])
        chromsCopy = copy.deepcopy(chromosomes)
        expectedChrom = self.ga.getMostFitChromosome(chromosomes)
        bestFitness = -math.inf
        actualChrom = None
        for chrom in chromsCopy:
            if chrom.fitness >  bestFitness:
                actualChrom = chrom
                bestFitness = chrom.fitness
        self.assertListEqual(expectedChrom.alleles, actualChrom.alleles)
        self.assertEqual(expectedChrom.fitness, actualChrom.fitness)
    
    def testSortChromosomes(self):
        chromosomes = self.ga.createChromosomes()
        for chrom in chromosomes:
            chrom.fitness = self.ga.f(chrom.alleles[0], chrom.alleles[1])
        chromosomes = self.ga.sortChromosomes(chromosomes)
        isSorted = True
        for i in range(1, len(chromosomes)):
            if chromosomes[i - 1].fitness < chromosomes[i].fitness:
                isSorted = False
                break
        self.assertIs(isSorted, True)

    def testSizeOfPopAfterCrossover(self):
        parents = self.ga.createChromosomes()
        offspring = self.ga.crossover(parents)
        self.assertEqual(len(offspring), len(parents) * OFFSPRING_MULTIPLIER)

    def testMutateNumberOfChanges(self):
        chromosomes = self.ga.createChromosomes()
        mutatedChroms = self.ga.mutate(copy.deepcopy(chromosomes))
        mutatedChromsCount = 0
        for i in range(len(chromosomes)):
            if chromosomes[i].alleles != mutatedChroms[i].alleles:
                print(f'TEST: {chromosomes[i].alleles} != {mutatedChroms[i].alleles}')
                mutatedChromsCount += 1
        print(f'{mutatedChromsCount} out of {len(chromosomes)} mutated.')
        variance = VARIANCE_PERCENTAGE*len(chromosomes)
        expectedMutations = self.ga.mutationRate * len(chromosomes)
        self.assertLessEqual(mutatedChromsCount, expectedMutations + variance)
        self.assertGreaterEqual(mutatedChromsCount, expectedMutations - variance)
    
    def testFitnessesSum(self):
        chromosomes = self.ga.createChromosomes()
        chromosomes = self.ga.setFitnesses(chromosomes)
        expectedSum = self.ga.getFitnessesSum(copy.deepcopy(chromosomes))
        actualSum = 0
        for chrom in chromosomes:
            actualSum += chrom.fitness
        self.assertEqual(expectedSum, actualSum)
    
    def testAvgFitness(self):
        chromosomes = self.ga.createChromosomes()
        chromosomes = self.ga.setFitnesses(chromosomes)
        expectedAvg = self.ga.getAvgFitness(chromosomes)
        actualAvg = 0
        for chrom in chromosomes:
            actualAvg += chrom.fitness
        actualAvg /= len(chromosomes)
        self.assertEqual(expectedAvg, actualAvg)
    
    def testSizeOfPopAfterSelect(self):
        chromosomes = self.ga.createChromosomes()
        parents = self.ga.select(copy.deepcopy(chromosomes))
        self.assertEqual(len(parents), len(chromosomes) / 2)

if __name__ == "__main__":
    unittest.main()