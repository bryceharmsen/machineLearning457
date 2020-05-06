import numpy as np
from mlp import mlp

def runxor():
    data = np.array([[0,0,0],[0,1,1],[1,0,1],[1,1,0]])
    print data[:,:2]
    print data[:,2:3]
    inputs = data[:,:2]
    targets = data[:,2:]
    percepter = mlp(data[:,:2], data[:,2:], 2)
    percepter.mlptrain(data[:,:2], data[:,2:], 0.2, 5001)
    percepter.confmat(inputs, targets)

if __name__ == "__main__":
    runxor()