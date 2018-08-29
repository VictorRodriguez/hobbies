import matplotlib.pyplot as plt
import numpy as np

def print_regresion(data,count,case):
    print("%s: regresion in value %s with regards to previus value %s"\
            % (case,str(data[count]),str(data[count-1])))

def detect_regresions(data,stdv_datail,HIB_flag):
    # detect regresion 
    regressions = []
    count = 0
    for value in np.nditer(data):
        if (count >= 1):
            if HIB_flag:
                # case for HIB
                case = "HIB"
                max_limit = data[count] + stdv_data[count]
                previous_limit = data[count -1] - stdv_data[count -1]
                if (max_limit < previous_limit):
                    regressions.append(count)
                    print_regresion(data,count,case)
            else:
                # case for LIB
                case = "LIB"
                min_limit = data[count] -stdv_data[count]
                previous_limit = data[count -1] + stdv_data[count -1]
                if (min_limit > previous_limit):
                    regressions.append(count)
                    print_regresion(data,count,case)
        count+=1
    return regressions

data = np.array([10, 10, 10, 12, 10,13])
stdv_data = np.array([1.2, 1.1, 0.9, 1.5, 1.2,1.1])
HIB_flag = False

regressions = detect_regresions(data,stdv_data,HIB_flag)

x = np.arange(1,data.size+1,1)
plt.errorbar(x, data, stdv_data, linestyle='-.', marker='*')

if regressions:
    for position in regressions:
        plt.annotate("regresion",(x[position], data[position]))

#plt.savefig('image.png')
#plt.show()
