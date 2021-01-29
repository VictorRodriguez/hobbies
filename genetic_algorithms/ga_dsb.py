import numpy as np
from geneticalgorithm import geneticalgorithm as ga

def f(X):
    pen = 0
    latency = 0
    threads = X[0]
    connections = X[1]
    if connections<threads:
        latency = 100000
    latency=(connections/(2*threads)) + pen
    return latency

varbound=np.array([[1,127],[1,255]])
vartype=np.array([['int'],['int']])

algorithm_param = {'max_num_iteration': 3000,\
                   'population_size':100,\
                   'mutation_probability':0.1,\
                   'elit_ratio': 0.01,\
                   'crossover_probability': 0.5,\
                   'parents_portion': 0.3,\
                   'crossover_type':'uniform',\
                   'max_iteration_without_improv':None}

model=ga(function=f,\
    dimension=2,\
    variable_type_mixed=vartype,\
    algorithm_parameters=algorithm_param,\
    variable_boundaries=varbound)

model.run()
