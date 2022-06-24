import sys
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

if len(sys.argv) > 1:
    clusters = int(sys.argv[1])
else:
    clusters = 6

df = pd.read_csv("pca.csv")
test_column = list(df.columns)[3]
print(test_column)

df = pd.read_csv("pca.csv", usecols = ['principal component 1','principal component 2'])

workload_name_df = pd.read_csv("pca.csv", usecols =[test_column])
workload_name = workload_name_df[test_column].values

kmeans = KMeans(n_clusters=clusters).fit(df)
centroids = kmeans.cluster_centers_
labels = kmeans.labels_
print(labels)
print(centroids)
df['labels'] = labels
df[test_column] = workload_name

print(df)

grouped_df = df.groupby("labels")
grouped_lists = grouped_df[test_column].apply(list)
grouped_lists = grouped_lists.reset_index()
print(grouped_lists.explode(test_column))
grouped_lists.explode(test_column).to_csv("clusters.csv")

plt.scatter(df['principal component 1'], df['principal component 2'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.title("Workload clustering based on similar pre silicon behavior")
plt.xlabel("Principal component 1")
plt.ylabel("Principal component 2")
plt.grid()
plt.show()

