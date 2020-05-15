import math
import numpy as np

class Objective:
    def __init__(self):
        pass
    
    def f(self, x, y):
        return np.sin(math.pi * 10 * x + 10/(1 + y**2)) \
               + np.log(x**2 + y**2)