import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn import linear_model
import pandas as pd

df_boston = pd.read_csv('BostonHousePrices.csv')


y = df_boston['Value'] # dependent variable
x = df_boston['Rooms'] # independent variable

x = sm.add_constant(x) # adding a constant
lm = sm.OLS(y,x).fit() # fitting the model

print(lm.predict(x))
print(lm.summary())

y_pred = 9.1021*x['Rooms'] - 34.6706

# plotting the data points
plt.figure(figsize=(12, 8), tight_layout=True)
sns.scatterplot(x=x['Rooms'], y=y)

#plotting the line
sns.lineplot(x=x['Rooms'],y=y_pred, color='red')

#axes
plt.xlim(0)
plt.ylim(0)
plt.savefig('linear_regression')
plt.show()
