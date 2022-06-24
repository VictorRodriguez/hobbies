 # clustering dataset
# determine k using elbow method

from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def calculate_elbow(df):

    x1 = df["principal component 1"].values
    x2 = df["principal component 2"].values

    # create new plot and data
    X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)

    # k means determine k
    distortions = []
    inertias = []

    K = range(1,10)
    for k in K:
        kmeanModel = KMeans(n_clusters=k).fit(X)
        kmeanModel.fit(X)
        distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])
        inertias.append(kmeanModel.inertia_)

    print(distortions)
    print(inertias)

    # Plot the elbow
    plt.plot(K, distortions, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Distortion')
    plt.title('The Elbow Method showing the optimal k')
    plt.savefig('distortion.png')
    plt.show()

    plt.plot(K, inertias, 'bx-')
    plt.xlabel('Values of K')
    plt.ylabel('Inertia')
    plt.title('The Elbow Method using Inertia')
    plt.savefig('intertia.png')
    plt.show()

def main():
    df = pd.read_csv("pca.csv")
    calculate_elbow(df)

if __name__ == "__main__":
    main()
