import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


features = ['cpu_bound','memory_bound','l3_bound', 'dram_bound', 'core_bound']

def get_explained_variance():

    # load dataset into Pandas DataFrame
    df = pd.read_csv('results.csv')
    print(df)

    # Standardizing the features

    # Separating out the features
    x = df.loc[:, features].values
    # Separating out the target
    y = df.loc[:,['test_name']].values

    x = StandardScaler().fit_transform(x)
    pca = PCA()
    principalComponents = pca.fit_transform(x)

    # Determine explained variance using explained_variance_ration_ attribute
    exp_var_pca = pca.explained_variance_ratio_

    print("pca.explained_variance_ratio_:")
    print(exp_var_pca)

    df = pd.DataFrame({'lab':features, 'val':exp_var_pca})

    ax = df.plot.bar(x='lab', y='val', rot=0)

    ax.set_ylabel('Explained variance ratio')
    ax.set_xlabel('Principal component index')
    ax.set_title('Explained variance')

    plt.show()

def get_PCA():

    # load dataset into Pandas DataFrame
    df = pd.read_csv('results.csv')
    print(df)

    # Separating out the features
    x = df.loc[:, features].values
    # Separating out the target
    y = df.loc[:,['test_name']].values

    # Standardizing the features
    x = StandardScaler().fit_transform(x)
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(x)

    principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])
    finalDf = pd.concat([principalDf, df[['test_name']]], axis = 1)
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
    plt.savefig('pca.png')
    plt.show()

get_explained_variance()
get_PCA()

