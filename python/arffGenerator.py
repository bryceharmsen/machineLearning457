import shutil
import util
from objective import Objective

def generateARFF(fileName, samples):
    fullDestFilePath = f'./project2/data/{fileName}.arff'
    shutil.copy2('./project2/starter.arff', fullDestFilePath)
    with open(fullDestFilePath, 'a') as arff:
        for sample in samples:
            arff.write(f'{sample[0]},{sample[1]},{sample[2]}\n')

if __name__ == "__main__":
    params = util.getParams('./project2/params/params.yaml')
    xDomain = [1, 100]
    yDomain = [1, 100]
    objective = Objective(xDomain, yDomain)
    trainingSamples = objective.getSamples(params['numSamples'])
    generateARFF('samples', objective.getSamples(params['numSamples']))