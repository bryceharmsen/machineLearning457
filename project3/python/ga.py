import abc
from typing import List

class Chrom:
    def __init__(self, alleles: List, fitness: float):
        self.alleles = alleles
        self.fitness = fitness

ChromList = List[Chrom]

class GA(metaclass=abc.ABCMeta):
    def __init__(self, generations: int, populationSize: int, mutationRate: float):
        self.populationSize = populationSize
        self.generations = generations
        self.mutationRate = mutationRate

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'createChromosomes') and
                callable(subclass.createChromosomes) and
                hasattr(subclass, 'select') and
                callable(subclass.select) and
                hasattr(subclass, 'crossover') and
                callable(subclass.crossover) and
                hasattr(subclass, 'mutate') and
                callable(subclass.mutate) and
                hasattr(subclass, 'setFitnesses') and
                callable(subclass.setFitnesses) and
                hasattr(subclass, 'getMostFitChromosome') and
                callable(subclass.getMostFitChromosome) or
                NotImplemented)
    
    @abc.abstractmethod
    def createChromosomes(self) -> ChromList:
        """Create chromosomes randomly based on user-defined parameters."""
        raise NotImplementedError

    @abc.abstractmethod
    def select(self, chromosomes: ChromList) -> ChromList:
        """Selects the best p percentage of chromosomes."""
        raise NotImplementedError

    @abc.abstractmethod
    def crossover(self, parents: ChromList) -> ChromList:
        """Performs crossover with random pairs of parent chromosomes."""
        raise NotImplementedError

    @abc.abstractmethod
    def mutate(self, offspring: ChromList) -> ChromList:
        """Mutates m percentage of chromsomes."""
        raise NotImplementedError

    @abc.abstractmethod
    def setFitnesses(self, chromosomes: ChromList) -> ChromList:
        """Sets fitness value for each Chrom object in list of chromosomes."""
        raise NotImplementedError

    @abc.abstractmethod
    def getMostFitChromosome(self, chromosomes: ChromList) -> Chrom:
        """Gets most fit chromosome from the list provided."""
        raise NotImplementedError

    def getNextGeneration(self, chromosomes: ChromList) -> ChromList:
        """Gets next generation of chromosomes using implemented select, crossover, and mutate."""
        parents = self.select(chromosomes)
        offspring = self.crossover(parents)
        offspring = self.mutate(offspring)
        return parents + offspring

    def run(self):
        '''Runs genetic algorithm for the number of generations defined in the object creation.'''
        chromosomes = self.createChromosomes()
        chromosomes = self.setFitnesses(chromosomes)
        bestChromByGen = [self.getMostFitChromosome(chromosomes)]
        for i in range(1, self.generations):
            chromosomes = self.getNextGeneration(chromosomes)
            bestChromByGen.append(self.getMostFitChromosome(chromosomes))
        #report most fit chromosome
        #report most fit for each generation
        return bestChromByGen