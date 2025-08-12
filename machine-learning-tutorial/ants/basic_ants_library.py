import math
import numpy as np
import matplotlib.pyplot as plt

# --- TSPLIB parser for coordinates ---
def parse_tsplib(filename):
    coords = []
    with open(filename, 'r') as file:
        read_nodes = False
        for line in file:
            if line.startswith("NODE_COORD_SECTION"):
                read_nodes = True
                continue
            if read_nodes:
                if line.strip() == "EOF":
                    break
                parts = line.strip().split()
                if len(parts) >= 3:
                    x = float(parts[1])
                    y = float(parts[2])
                    coords.append((x, y))
    return coords

# --- Distance calculation ---
def euclidean_distance_matrix(coords):
    n = len(coords)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = math.sqrt(
                (coords[i][0] - coords[j][0]) ** 2 + (coords[i][1] - coords[j][1]) ** 2)
    return dist_matrix

# --- ACO algorithm with convergence tracking ---
def ant_colony_optimization(dist_matrix, n_ants, n_iterations, alpha, beta, evaporation_rate, pheromone_deposit):
    n_nodes = dist_matrix.shape[0]
    pheromone = np.ones((n_nodes, n_nodes))
    best_path = None
    best_path_length = float('inf')
    best_lengths = []  # Track best length per iteration

    for iteration in range(n_iterations):
        all_paths = []
        for ant in range(n_ants):
            path = [np.random.randint(n_nodes)]
            while len(path) < n_nodes:
                current = path[-1]
                allowed = list(set(range(n_nodes)) - set(path))
                pheromone_list = np.array([pheromone[current][j] for j in allowed])
                heuristic_list = np.array([1.0 / dist_matrix[current][j] if dist_matrix[current][j] > 0 else 0 for j in allowed])
                probs = (pheromone_list ** alpha) * (heuristic_list ** beta)
                probs = probs / probs.sum()
                next_node = np.random.choice(allowed, p=probs)
                path.append(next_node)
            path_length = sum(dist_matrix[path[i]][path[i+1]] for i in range(n_nodes - 1))
            path_length += dist_matrix[path[-1]][path[0]]  # Return to start
            all_paths.append((path, path_length))

            if path_length < best_path_length:
                best_path_length = path_length
                best_path = path

        # Pheromone evaporation
        pheromone *= (1 - evaporation_rate)

        # Pheromone update based on paths
        for path, length in all_paths:
            for i in range(n_nodes - 1):
                pheromone[path[i]][path[i+1]] += pheromone_deposit / length
            pheromone[path[-1]][path[0]] += pheromone_deposit / length

        best_lengths.append(best_path_length)
        print(f"Iteration {iteration+1}/{n_iterations}, Best path length: {best_path_length:.2f}")

    return best_path, best_path_length, best_lengths

# --- Visualization for best path ---
def plot_path(coords, path):
    x = [coords[i][0] for i in path] + [coords[path[0]][0]]
    y = [coords[i][1] for i in path] + [coords[path[0]][1]]
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'b-', marker='o')
    plt.title("Best path found by ACO on TSPLIB dataset")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()

# --- Visualization for convergence ---
def plot_convergence(best_lengths):
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, len(best_lengths) + 1), best_lengths, marker='o')
    plt.title('ACO Convergence Over Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Best Path Length')
    plt.grid(True)
    plt.show()

# --- Main ---

# 1) Parse coordinates from TSPLIB file (update path if needed)
coords = parse_tsplib("att532.tsp")

# 2) Compute distance matrix
dist_matrix = euclidean_distance_matrix(coords)

# 3) Run ACO with convergence tracking
best_path, best_length, best_lengths = ant_colony_optimization(
    dist_matrix,
    n_ants=20,
    n_iterations=10,
    alpha=5.0,
    beta=1.0,
    evaporation_rate=0.5,
    pheromone_deposit=100
)

print(f"Best path length: {best_length:.2f}")

# 4) Plot results
plot_convergence(best_lengths)
plot_path(coords, best_path)

