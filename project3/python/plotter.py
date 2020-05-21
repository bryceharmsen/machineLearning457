from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import util

def plot3d(xDomain, yDomain, objectiveFunc, savePath = '.'):
    figure = plt.figure()
    axis = figure.gca(projection='3d')

    x = np.linspace(xDomain[0], xDomain[1], 1000)
    y = np.linspace(yDomain[0], yDomain[1], 1000)
    x, y = np.meshgrid(x, y)
    z = objectiveFunc(x, y)

    surface = axis.plot_surface(x, y, z, cmap=cm.jet,
                                linewidth=0, antialiased=False)

    figure.colorbar(surface, shrink=0.5, aspect=5,)
    plt.savefig(f'{savePath}/objectivePlot.png')
    #plt.show()
    plt.show(block=False)
    plt.pause(2)
    plt.close()

def plot2dTimeSeries(values, title='series', xLabel='time', yLabel='values', savePath='.'):
    """Plot 2d time series"""
    plt.plot(values)
    plt.ylabel(yLabel)
    plt.xlabel(xLabel)
    plt.xticks(np.linspace(0, len(values), 11))
    plt.title(title)
    plt.savefig(f'{savePath}/{title}.png')
    plt.show(block=False)
    plt.pause(2)
    plt.close()

def plot2dScatter(points, title='scatter', savePath='.'):
    colors = cm.rainbow(np.linspace(0, 1, len(points)))
    for pt, c in zip(points, colors):
        plt.scatter(*pt, color=c)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(title)
    plt.savefig(f'{savePath}/{title}.png')
    plt.show(block=False)
    plt.pause(2)
    plt.close()