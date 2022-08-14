import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from distortion import *
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import sys
from sklearn.manifold import TSNE



def get_explained_variance(X_std):

    pca = PCA()
    principalComponents = pca.fit_transform(X_std)

    # Determine explained variance using explained_variance_ration_ attribute
    exp_var_pca = pca.explained_variance_ratio_

    cum_sum_eigenvalues = np.cumsum(exp_var_pca)

    plt.bar(range(0,len(exp_var_pca)), exp_var_pca, alpha=0.5, align='center', label='Individual explained variance')
    plt.step(range(0,len(cum_sum_eigenvalues)), cum_sum_eigenvalues, where='mid',label='Cumulative explained variance')
    plt.ylabel('Explained variance ratio')
    plt.xlabel('Principal component index')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig('variance.png')
    plt.show()

def get_eigen(X_std):

    mean_vec = np.mean(X_std, axis=0)
    cov_mat = (X_std - mean_vec).T.dot((X_std - mean_vec)) / (X_std.shape[0]-1)
    eig_vals, eig_vecs = np.linalg.eig(cov_mat)

    print(f'Covariance matrix \n {cov_mat}')
    print(f'Eigenvectors \n {eig_vecs}')
    print(f'Eigenvalues \n {eig_vals}')


def get_TSNE(df, features, test_column):
    # Separating out the features
    x = df.loc[:, features].values
    # Separating out the target
    y = df.loc[:,[test_column]].values
    cov_mat = np.cov(x.T)
    eig_vals, eig_vecs = np.linalg.eig(cov_mat)

    # Standardizing the features
    X_std = StandardScaler().fit_transform(x)
    get_eigen(X_std)

    tsne = TSNE(n_components=2, verbose=1, perplexity = 10)
    tsne_results = tsne.fit_transform(X_std)
    print(tsne_results)

    principalDf = pd.DataFrame(data = tsne_results, columns = ['TSNE 1', 'TSNE 2'])
    finalDf = pd.concat([principalDf, df[['test_name']]], axis = 1)
    finalDf.to_csv("tsne.csv")
    print(finalDf)

    fig = plt.figure(figsize=(16,10))
    ax = fig.add_subplot(1,1,1)

    ax.set_xlabel('TSNE 1', fontsize = 15)
    ax.set_ylabel('TSNE 2', fontsize = 15)
    ax.set_title('2 component TSNE', fontsize = 20)
    ax.scatter(finalDf['TSNE 1']
                   ,finalDf['TSNE 2']
                   , c = 'g'
                   , s = 50)

    for i, label in enumerate(y):
        plt.annotate(label, (finalDf['TSNE 1'][i], finalDf['TSNE 2'][i]))

    ax.grid()
    plt.savefig('tsna.png')
    plt.show()

def get_PCA(df, features, test_column):
    print(df)
    # Separating out the features
    x = df.loc[:, features].values
    # Separating out the target
    y = df.loc[:,[test_column]].values
    print(x)

    cov_mat = np.cov(x.T)
    print(cov_mat)
    eig_vals, eig_vecs = np.linalg.eig(cov_mat)
    print('Eigenvectors \n%s' %eig_vecs)
    print('\nEigenvalues \n%s' %eig_vals)


    # Standardizing the features
    X_std = StandardScaler().fit_transform(x)

    get_eigen(X_std)

    get_explained_variance(X_std)

    pca = PCA(n_components=2)

    principalComponents = pca.fit_transform(X_std)

    principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])
    finalDf = pd.concat([principalDf, df[['test_name']]], axis = 1)
    finalDf.to_csv("pca.csv")
    print(finalDf)

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


def main():
    df = pd.read_csv('results_icx_norm.csv')
    features = list(df.columns)[1:]
    test_column = list(df.columns)[0]

    get_PCA(df, features,test_column)
    get_TSNE(df, features,test_column)
    calculate_elbow(pd.read_csv("pca.csv"))

if __name__ == "__main__":
    main()


