import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

FILE = "tsne.csv"
clusters = 6

if len(sys.argv) > 1:
    FILE = sys.argv[1]
    print(FILE)
    clusters = int(sys.argv[2])

df = pd.read_csv(FILE)
test_column = list(df.columns)[3]
print(test_column)

if "pca" in FILE:
    df = pd.read_csv(FILE, usecols = ['principal component 1','principal component 2'])
elif "tsne" in FILE:
    df = pd.read_csv(FILE, usecols = ['TSNE 1','TSNE 2'])
else:
    sys.exit(-1)

workload_name_df = pd.read_csv(FILE, usecols =[test_column])
workload_name = workload_name_df[test_column].values

kmeans = KMeans(init="k-means++", n_clusters=clusters).fit(df)
centroids = kmeans.cluster_centers_
labels = kmeans.labels_
X_dist = (kmeans.transform(df))

distance = []

for inner_list in X_dist:
    distance.append((min(inner_list)))

print(labels)
print(distance)
print(centroids)
df['PRED'] = labels
df[test_column] = workload_name
df['distance'] = distance
print(df)
df.to_csv("test.csv")

y = df.loc[:,['test_name']].values

grouped_df = df.groupby("PRED")
grouped_lists = grouped_df[test_column].apply(list)
grouped_lists = grouped_lists.reset_index()
print(grouped_lists.explode(test_column))
grouped_lists.explode(test_column).to_csv("clusters.csv")

plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
if "pca" in FILE:
    plt.scatter(df['principal component 1'], df['principal component 2'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
    for i, label in enumerate(y):
        plt.annotate(label, (df['principal component 1'][i], df['principal component 2'][i]))
elif "tsne" in FILE:
    plt.scatter(df['TSNE 1'], df['TSNE 2'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
    for i, label in enumerate(y):
        plt.annotate(label, (df['TSNE 1'][i], df['TSNE 2'][i]))
else:
    sys.exit(-1)

plt.xlabel("component 1")
plt.ylabel("component 2")
plt.grid()
plt.savefig('clustering.png')
plt.show()

