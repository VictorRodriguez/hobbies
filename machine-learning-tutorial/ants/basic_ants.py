import numpy as np
import matplotlib.pyplot as plt

# --- Problem setup ---
coords = np.array([
    [0, 0], [2, 0], [3, 1], [2, 2], [0, 2], [1, 3], [3, 3], [4, 0]
])
n_cities = len(coords)
dist_matrix = np.sqrt(((coords[:, None, :] - coords[None, :, :])**2).sum(axis=2))

# Parameters (tuned for gradual convergence)
n_ants = 20
n_iterations = 40
alpha, beta, evaporation = 1.0, 1.0, 0.8
pheromone = np.ones((n_cities, n_cities)) * 0.1  # lower initial pheromone

best_length = np.inf
best_path = None
best_lengths_over_time = []

# --- Helper functions ---
def path_length(path):
    return sum(dist_matrix[path[i], path[(i+1)%n_cities]] for i in range(n_cities))

def plot_state(iteration, pheromone, best_path, best_length):
    plt.figure(figsize=(5, 5))
    max_pher = pheromone.max()
    for i in range(n_cities):
        for j in range(i+1, n_cities):
            lw = 0.3 + 3*(pheromone[i, j] / max_pher)
            plt.plot([coords[i,0], coords[j,0]], [coords[i,1], coords[j,1]],
                     color='gray', alpha=0.5, linewidth=lw)
    plt.scatter(coords[:,0], coords[:,1], c='red', s=100, zorder=5)
    for idx, (x, y) in enumerate(coords):
        plt.text(x+0.05, y+0.05, str(idx), fontsize=10)
    for i in range(n_cities):
        a, b = best_path[i], best_path[(i+1)%n_cities]
        plt.plot([coords[a,0], coords[b,0]], [coords[a,1], coords[b,1]],
                 color='blue', linewidth=2.5)
    plt.title(f"Iteration {iteration}\nBest length = {best_length:.2f}")
    plt.axis("equal")
    plt.axis("off")
    plt.show()

# --- Main loop ---
for it in range(n_iterations):
    all_paths = []
    all_lengths = []
    for _ in range(n_ants):
        path = [np.random.randint(n_cities)]
        while len(path) < n_cities:
            i = path[-1]
            mask = np.ones(n_cities, dtype=bool)
            mask[path] = False
            probs = (pheromone[i, mask]**alpha) * ((1/dist_matrix[i, mask])**beta)
            probs /= probs.sum()
            next_city = np.where(mask)[0][np.random.choice(len(probs), p=probs)]
            path.append(next_city)
        length = path_length(path)
        all_paths.append(path)
        all_lengths.append(length)
        if length < best_length:
            best_length, best_path = length, path
    # --- Pheromone update ---
    pheromone *= (1 - evaporation)
    for path, length in zip(all_paths, all_lengths):
        for i in range(n_cities):
            pheromone[path[i], path[(i+1)%n_cities]] += 1.0 / length
    best_lengths_over_time.append(best_length)
    #plot_state(it+1, pheromone, best_path, best_length)

# Convergence curve
plt.figure(figsize=(6,4))
plt.plot(range(1, n_iterations+1), best_lengths_over_time, marker='o')
plt.xlabel("Iteration")
plt.ylabel("Best Path Length")
plt.title("ACO Convergence")
plt.grid(True)
plt.show()

print("Best path:", best_path, "length:", best_length)

