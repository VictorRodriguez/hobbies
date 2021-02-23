import numpy as np
import math
from geneticalgorithm import geneticalgorithm as ga
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

x = []
y = []
z = []

def f(X):
    global x
    global y
    global z
    dim=len(X)

    t1=0
    t2=0
    for i in range (0,dim):
        t1+=X[i]**2
        t2+=math.cos(2*math.pi*X[i])

    OF=20+math.e-20*math.exp((t1/dim)*-0.2)-math.exp(t2/dim)

    x.append(t1/dim)
    y.append(t2/dim)
    z.append(OF)

    return OF

varbound=np.array([[-32.768,32.768]]*2)

model=ga(function=f,dimension=2,variable_type='real',variable_boundaries=varbound)

model.run()

print(len(x))
print(len(y))
print(len(z))



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x, y, z, c='y', marker='o')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()

