from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import util

def plot3d(xDomain, yDomain, objectiveFunc, savePath = '.', **kwargs):
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

def plot2d(values, title='', xLabel='time', yLabel='values', savePath='.', tickFreq=1):
    """Plot 2d time series"""
    plt.plot(values)
    plt.ylabel(yLabel)
    plt.xlabel(xLabel)
    ticks = []
    for i in range(len(values)):
        if i % tickFreq == 0:
            ticks.append(i)
    plt.xticks(ticks)
    plt.title(title)
    plt.savefig(f'{savePath}/{title}.png')
    plt.show(block=False)
    plt.pause(1)
    plt.close()