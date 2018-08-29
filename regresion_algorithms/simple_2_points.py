import matplotlib.pyplot as plt
import numpy as np

x = np.array([1,2,3,4,5,6])
y = np.array([10, 10, 10, 12, 10,13])
e = np.array([1.2, 1.1, 0.9, 1.5, 1.2,1.1])


# detect regresion 
count = 0
for value in np.nditer(x):
    if (count >= 1):
        # case for LIB
        min_limit = y[count] -e[count]
        previous_limit = y[count -1] + e[count -1]
        if (min_limit > previous_limit):
            print("LIB: regresion in value %s with regards to previus value %s" % 
                    (str(y[count]),str(y[count-1])))
    count+=1

plt.errorbar(x, y, e, linestyle='-.', marker='*')
plt.annotate("regresion",(x[5], y[5]))

plt.savefig('image.png')
plt.show()
