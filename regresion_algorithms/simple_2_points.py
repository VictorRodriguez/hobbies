import matplotlib.pyplot as plt
import numpy as np

def detect_regresions(data,stdv_data):
    # detect regresion 
    regressions = []
    count = 0
    for value in np.nditer(x):
        if (count >= 1):
            # case for LIB
            min_limit = data[count] -stdv_data[count]
            previous_limit = data[count -1] + stdv_data[count -1]
            if (min_limit > previous_limit):
                regressions.append(count)
                print("LIB: regresion in value %s with regards to previus \
                        value %s" % (str(data[count]),str(stdv_data[count-1])))
        count+=1
    return regressions

data = np.array([10, 10, 10, 12, 10,13])
stdv_data = np.array([1.2, 1.1, 0.9, 1.5, 1.2,1.1])
x = np.arange(1,data.size+1,1)
regressions = detect_regresions(data,stdv_data)
plt.errorbar(x, data, stdv_data, linestyle='-.', marker='*')

if regressions:
    for position in regressions:
        plt.annotate("regresion",(x[position], data[position]))

plt.savefig('image.png')
plt.show()
