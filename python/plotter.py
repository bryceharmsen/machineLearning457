from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import util
from objective import Objective

def plotActual(xDomain, yDomain, objectiveFunc, savePath = '.'):
    figure = plt.figure()
    axis = figure.gca(projection='3d')

    x = np.arange(xDomain[0], xDomain[1], 0.5)
    y = np.arange(yDomain[0], yDomain[1], 0.5)
    x, y = np.meshgrid(x, y)
    z = objectiveFunc(x, y)

    surface = axis.plot_surface(x, y, z, cmap=cm.jet,
                                linewidth=0, antialiased=False)

    figure.colorbar(surface, shrink=0.5, aspect=5,)
    plt.savefig(f'{savePath}/objectivePlot.png')
    plt.show(block=False)
    plt.pause(2)
    plt.close()

if __name__ == "__main__":
    params = util.getParams('./project2/params/params.yaml')
    xDomain = [1, 100]
    yDomain = [1, 100]
    objective = Objective(xDomain, yDomain)
    plotActual(xDomain, yDomain, objective.calculate, params['resultsPath'])
