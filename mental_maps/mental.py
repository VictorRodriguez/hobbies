import networkx as nx
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample data (descriptions of dog and cat breeds)
breeds = {
    "Labrador Retriever": "Friendly and outgoing, Labs play well with others.",
    "Poodle": "Poodles are known for their intelligence and hypoallergenic coat.",
    "German Shepherd": "Confident and courageous, German Shepherds are versatile working dogs.",
    "Persian Cat": "Persians are known for their quiet and sweet personalities.",
    "Siamese Cat": "Siamese cats are social, vocal, and affectionate.",
    "Maine Coon": "Maine Coons are large, friendly, and known for their tufted ears."
}

# Create a list of breed names and descriptions
breed_names = list(breeds.keys())
descriptions = list(breeds.values())

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(descriptions)

# Calculate cosine similarity matrix
similarity_matrix = cosine_similarity(X)

# Create Graph
G = nx.Graph()
for i, breed in enumerate(breed_names):
    G.add_node(i, label=breed)

# Add edges based on similarity (only if similarity is above a certain threshold)
threshold = 0.1  # Adjust this threshold based on the desired level of connectivity
for i in range(len(breed_names)):
    for j in range(i+1, len(breed_names)):
        if similarity_matrix[i, j] > threshold:
            G.add_edge(i, j, weight=similarity_matrix[i, j])

# Assign colors to nodes based on type (dogs or cats)
node_colors = ['lightblue' if 'Cat' not in breed_names[i] else 'lightgreen' for i in range(len(breed_names))]

# Draw Graph
pos = nx.spring_layout(G, seed=42)  # Fixed seed for reproducibility
nx.draw(G, pos, with_labels=True, labels={i: breed for i, breed in enumerate(breed_names)}, node_color=node_colors, node_size=3000, font_size=10)
plt.title("Mental Map of Dog and Cat Breeds")
plt.show()

