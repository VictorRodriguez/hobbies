import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


# Set pandas options to display all rows and columns without truncation
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Load the Iris dataset
df = pd.read_csv('iris.csv')

# Extract features
features = df.drop(columns=['Species'])  # Assuming the species column is the label

# Perform PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(features)

# Convert the PCA result to a DataFrame
pca_df = pd.DataFrame(pca_result, columns=['PC1', 'PC2'])

# Perform K-means clustering
kmeans = KMeans(n_clusters=6, random_state=42)  # Assuming 3 clusters for Iris dataset
kmeans.fit(pca_df)

# Add cluster labels to the PCA DataFrame
pca_df['cluster'] = kmeans.labels_

# Print the PCA components
print("PCA Components:")
print(pca_df)

# Plot the PCA result with cluster assignments
plt.scatter(pca_df['PC1'], pca_df['PC2'], c=pca_df['cluster'], cmap='viridis')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA of Iris Dataset with K-means Clusters')
plt.colorbar(label='Cluster')
plt.show()


# Range of cluster numbers to test
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
plt.show()

# Add the original index to the DataFrame
pca_df['index'] = df.index

# Print the element ID and the assigned cluster
print("Element ID and Assigned Cluster:")
print(pca_df[['index', 'cluster']])

