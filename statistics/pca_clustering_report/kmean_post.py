import sys
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

#Data = {'x': [25,34,22,27,33,33,31,22,35,34,67,54,57,43,50,57,59,52,65,47,49,48,35,33,44,45,38,43,51,46],
#        'y': [79,51,53,78,59,74,73,57,69,75,51,32,40,47,53,36,35,58,59,50,25,20,14,12,20,5,29,27,8,7]
#       }

#df = DataFrame(Data,columns=['x','y'])

if len(sys.argv) > 1:
    clusters = int(sys.argv[1])
else:
    clusters = 6

df = pd.read_csv("pca.csv", usecols = ['principal component 1','principal component 2'])

workload_name_df = pd.read_csv("pca.csv", usecols =['test_name'])
workload_name = workload_name_df['test_name'].values

kmeans = KMeans(n_clusters=clusters).fit(df)
centroids = kmeans.cluster_centers_
labels = kmeans.labels_
print(labels)
print(centroids)
df['labels'] = labels
df['test_name'] = workload_name

print(df)

grouped_df = df.groupby("labels")
grouped_lists = grouped_df["test_name"].apply(list)
grouped_lists = grouped_lists.reset_index()
print(grouped_lists.explode('test_name'))
grouped_lists.to_csv("clusters.csv")

plt.scatter(df['principal component 1'], df['principal component 2'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.title("Workload clustering based on similar post silicon behavior")
plt.xlabel("Principal component 1")
plt.ylabel("Principal component 2")
plt.grid()
plt.show()


