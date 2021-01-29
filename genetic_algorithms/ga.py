import numpy as np
import math
from geneticalgorithm import geneticalgorithm as ga

def f(X):

    dim=len(X)

    OF=0
    for i in range (0,dim):
        OF+=(X[i]**2)-10*math.cos(2*math.pi*X[i])+10

    return OF


varbound=np.array([[-5.12,5.12]]*2)

model=ga(function=f,dimension=2,variable_type='real',variable_boundaries=varbound)

model.run()

