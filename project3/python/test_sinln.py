import unittest
from sinln import SinLn, Chrom
from types import SimpleNamespace
import numpy as np
import math
import util
import copy

NUM_ALLELES = 2
OFFSPRING_MULTIPLIER = 2

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
        chromosomes = self.ga.createChromosomes()
        nextGenChroms = self.ga.crossover(chromosomes)
        self.assertEqual(len(nextGenChroms), len(chromosomes) * OFFSPRING_MULTIPLIER)

if __name__ == "__main__":
    unittest.main()