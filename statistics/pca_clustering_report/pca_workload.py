import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# load dataset into Pandas DataFrame
df = pd.read_csv('out.csv')
print(df)

features = ['arithmetic','branch','store_counter','other_counter']
# Separating out the features
x = df.loc[:, features].values
print(x)

# Separating out the target
y = df.loc[:,['workload_name']].values
#print(y)

# Standardizing the features
x = StandardScaler().fit_transform(x)
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
print("pca.explained_variance_ratio_:")
print(pca.explained_variance_ratio_)
principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])
finalDf = pd.concat([principalDf, df[['workload_name']]], axis = 1)
print(finalDf)
finalDf.to_csv("pca.csv")

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
ax.scatter(finalDf['principal component 1']
               , finalDf['principal component 2']
               , c = 'b'
               , s = 50)

for i, label in enumerate(y):
    plt.annotate(label, (finalDf['principal component 1'][i], finalDf['principal component 2'][i]))

ax.grid()
plt.show()

