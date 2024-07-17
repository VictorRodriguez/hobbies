import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score


# Set pandas options to display all rows and columns without truncation
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Load the Iris dataset
df = pd.read_csv('iris.csv')

# Extract features
features = df.drop(columns=['Id','Species'])

# Perform PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(features)

# Convert the PCA result to a DataFrame
pca_df = pd.DataFrame(pca_result, columns=['PC1', 'PC2'])

# Calculate inertia to find optimal number of clusters
cluster_range = range(1, 11)
inertias = []

for k in cluster_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(pca_df)
    inertias.append(kmeans.inertia_)
    print(f'Number of Clusters: {k}, Inertia: {kmeans.inertia_}')

# Plot the inertia vs. number of clusters
plt.plot(cluster_range, inertias, marker='o')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.title('Inertia per Cluster Count')
plt.savefig('inertia.png')

# Perform K-means clustering
kmeans = KMeans(n_clusters=6, random_state=42)  # Assuming 3 clusters for Iris dataset
kmeans.fit(pca_df)
labels = kmeans.labels_

# Get the centroids
centroids = kmeans.cluster_centers_

# Print all centroids
print("All centroids:\n", centroids)

# Add cluster labels to the PCA DataFrame
pca_df['cluster'] = kmeans.labels_

# Print the PCA components
print("PCA Components:")
print(pca_df)

# Plot the PCA result with cluster assignments and centroids
plt.figure(figsize=(8, 6))

# Scatter plot of PCA components with cluster assignments
plt.scatter(pca_df['PC1'], pca_df['PC2'], c=pca_df['cluster'], cmap='viridis', alpha=0.5, label='Data Points')

# Plot centroids
plt.scatter(centroids[:, 0], centroids[:, 1], marker='x', color='r', s=100, label='Centroids')

plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA of Dataset with K-means Clusters and Centroids')
plt.colorbar(label='Cluster')
plt.legend()
plt.savefig('clusters.png')


# Add the original index to the DataFrame
pca_df['index'] = df.index

# Print the element ID and the assigned cluster
print("Element ID and Assigned Cluster:")
print(pca_df[['index', 'cluster']])


# Calculate metrics
silhouette_avg = silhouette_score(pca_df, labels)
db_index = davies_bouldin_score(pca_df, labels)
ch_index = calinski_harabasz_score(pca_df, labels)
average_inertia = kmeans.inertia_ / kmeans.n_clusters

print(f"Silhouette Score: {silhouette_avg}")
print(f"Davies-Bouldin Index: {db_index}")
print(f"Calinski-Harabasz Index: {ch_index}")
print(f"Average Inertia: {average_inertia}")

