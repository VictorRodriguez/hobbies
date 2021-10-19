#https://vitalflux.com/pca-explained-variance-concept-python-example/

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# load dataset into Pandas DataFrame
df = pd.read_csv('workloads.csv')

features = ['arithmetic','store','branch','other']
x = df.loc[:, features].values

y = df.loc[:,['workload_name']].values

# Standardizing the features
x = StandardScaler().fit_transform(x)

# Instantiate PCA
pca = PCA()

# Determine transformed features
X_train_pca = pca.fit_transform(x)

# Determine explained variance using explained_variance_ration_ attribute
exp_var_pca = pca.explained_variance_ratio_

df = pd.DataFrame({'lab':features, 'val':exp_var_pca})

ax = df.plot.bar(x='lab', y='val', rot=0)

ax.set_ylabel('Explained variance ratio')
ax.set_xlabel('Principal component index')
ax.set_title('Explained variance')

plt.show()

"""
# Cumulative sum of eigenvalues; This will be used to create step plot
# for visualizing the variance explained by each principal component.
cum_sum_eigenvalues = np.cumsum(exp_var_pca)

# Create the visualization plot
plt.bar(range(0,len(exp_var_pca)), exp_var_pca, alpha=0.5, align='center', label='Individual explained variance')
plt.step(range(0,len(cum_sum_eigenvalues)), cum_sum_eigenvalues, where='mid',label='Cumulative explained variance')
plt.ylabel('Explained variance ratio')
plt.xlabel('Principal component index')
plt.legend(loc='best')
plt.tight_layout()
plt.show()
"""
