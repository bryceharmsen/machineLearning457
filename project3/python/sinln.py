import sys
import math
import numpy as np
import util
from ga_objective import GA, Chrom, ChromList

class SinLn(GA):
    def __init__(self, params):
        self.populationSize = params['populationSize']
        super().__init__(params)
    
    def f(self, x, y):
        return np.sin(math.pi * 10 * x + 10/(1 + y**2)) \
               + np.log(x**2 + y**2)

    def createChromosomes(self) -> ChromList:
        return [Chrom([np.random.uniform(0,1)], 0) for _ in range(self.populationSize)]

    def select(self, chromosomes: ChromList) -> ChromList:
        pass

    def crossover(self, parents: ChromList) -> ChromList:
        pass

    def mutate(self, offspring: ChromList) -> ChromList:
        pass

    def setFitnesses(self, chromosomes: ChromList) -> ChromList:
        pass

    def getMostFitChromosome(self, chromosomes: ChromList) -> Chrom:
        pass
        
if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print(f'Proper use:\n\tpython3 {sys.argv[0]} PARAM_FILENAME.yaml')
    params = util.getParams(sys.argv[1])
    ga = SinLn(params)
    ga.run()