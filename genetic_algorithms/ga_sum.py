import numpy as np
from geneticalgorithm import geneticalgorithm as ga

def f(X):
    return np.sum(X)


varbound=np.array([[0,10]]*3)

#model=ga(function=f,dimension=3,variable_type='real',variable_boundaries=varbound)
#model=ga(function=f,dimension=3,variable_type='int',variable_boundaries=varbound)
model=ga(function=f,dimension=30,variable_type='bool')
model.run()
