from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# generate synthetic two-dimensional data
X, y = make_blobs(random_state=1)

# specify the range of cluster numbers to consider
min_clusters = 2
max_clusters = 10
cluster_range = range(min_clusters, max_clusters + 1)

# calculate inertia for each cluster number
inertia_values = []
for n_clusters in cluster_range:
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(X)
    inertia_values.append(kmeans.inertia_)

# plot the inertia values over the range of cluster numbers
plt.plot(cluster_range, inertia_values, marker='o')
plt.title('Inertia vs. Number of Clusters')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.xticks(cluster_range)
plt.grid(True)
plt.show()

