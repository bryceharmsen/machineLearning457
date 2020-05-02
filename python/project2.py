import math
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import util

def objective(x, y):
    return np.sin(math.pi * 10 * x + 10/(1 + y**2)) \
           + np.log(x**2 + y**2)

#should the objective function be passed
#to the mlp as a param in the constructor?
#is that general enough?

def plotActual(xDomain, yDomain, objectiveFunc, savePath = '.'):
    figure = plt.figure()
    axis = figure.gca(projection='3d')

    x = np.arange(xDomain[0], xDomain[1], 0.1)
    y = np.arange(yDomain[0], yDomain[1], 0.1)
    x, y = np.meshgrid(x, y)
    z = objectiveFunc(x, y)

    surface = axis.plot_surface(x, y, z, cmap=cm.jet,
                                linewidth=0, antialiased=False)

    figure.colorbar(surface, shrink=0.5, aspect=5)
    plt.savefig(f'{savePath}/objectivePlot.png')
    plt.show(block=False)
    plt.pause(2)
    plt.close()

params = util.getParams('./project2/params/params.yaml')
plotActual([1, 100], [1,100], objective, params['resultsPath'])