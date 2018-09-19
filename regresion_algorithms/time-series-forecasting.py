from pandas import read_csv
from pandas import datetime
from sklearn.metrics import mean_squared_error
from math import sqrt
from matplotlib import pyplot as plt
import numpy as np

# calculate the average STDV of the history
average_stdv = 150

def detect_regresions(data,prediction,average_stdv):
    regressions = []
    count = 0
    for value in np.nditer(data):
        distance = abs(data[count] - prediction[count])
        if distance > average_stdv:
            regressions.append(count)
        count+=1
    return regressions

# load dataset
def parser(x):
	return datetime.strptime('190'+x, '%Y-%m')

series = read_csv('shampoo-sales.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)

# split data into train and test
# The first two years of data will be taken for the training dataset and the
# remaining one year of data will be used for the test set.
X = series.values
train, test = X[0:-12], X[-12:]

# walk-forward validation
history = [x for x in train]
predictions = list()

for i in range(len(test)):
	# make prediction
	predictions.append(history[-1])
	# observation
	history.append(test[i])

# report performance
rmse = sqrt(mean_squared_error(test, predictions))
print('RMSE: %.3f' % rmse)

regressions = detect_regresions(test,predictions,average_stdv)
print(regressions)

x = np.arange(0,test.size,1)

plt.errorbar(x, test, average_stdv, linestyle='-.', marker='*',label="real data")

if regressions:
    for position in regressions:
        plt.annotate("regresion",(x[position], test[position]))
# if you want to see the full data
#plt.plot(series)
plt.plot(predictions,label="predictions")
plt.legend(loc='best')

plt.savefig('image.png')
plt.show()

