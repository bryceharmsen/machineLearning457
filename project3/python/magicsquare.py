import sys
import math
import numpy as np
import util
from ga import GA, Chrom, ChromList

class MagicSquare(GA):
    def __init__(self, generations, populationSize, mutationRate):
        super(MagicSquare, self).__init__(generations, populationSize, mutationRate)

    def createChromosomes(self) -> ChromList:
        """Create chromosomes randomly based on user-defined parameters."""
        pass

    def select(self, chromosomes: ChromList) -> ChromList:
        """Selects the best p percentage of chromosomes."""
        pass

    def crossover(self, parents: ChromList) -> ChromList:
        """Performs crossover with random pairs of parent chromosomes."""
        pass

    def mutate(self, offspring: ChromList) -> ChromList:
        """Mutates m percentage of chromsomes."""
        pass

    def setFitnesses(self, chromosomes: ChromList) -> ChromList:
        """Sets fitness value for each Chrom object in list of chromosomes."""
        pass

    def getMostFitChromosome(self, chromosomes: ChromList) -> Chrom:
        """Gets most fit chromosome from the list provided."""
        pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f'Proper use:\n\tpython3 {sys.argv[0]} PARAM_FILENAME.yaml')
    params = util.getParams(sys.argv[1])
    ga = MagicSquare(params.generations, params.populationSize, params.mutationRate)
    ga.run()