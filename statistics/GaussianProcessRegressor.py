import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma

# 1. Simulate Initial Variances for 30 Washing Machines
num_washing_machines = 30
num_variables = 14

# Generate random test results (each machine has 14 test variables)
test_results = np.random.rand(num_washing_machines, num_variables) * 10  # Simulated sensor data
noise_level = 10.0  # Adjust this value to control noise intensity
test_results += np.random.normal(loc=0, scale=noise_level, size=test_results.shape)

# Compute variance for each washing machine
mean_variance = np.var(test_results, axis=1)

# 2. Select 3 Washing Machines with the Highest Variance
top_3_indices = np.argsort(mean_variance)[-3:]  # Get top 3 highest variance machines
selected_variances = mean_variance[top_3_indices]

# 3. Fit a Gamma Distribution Using **All 30 Machines**
shape, loc, scale = gamma.fit(mean_variance)  # Now includes all machines

# 4. Function to Determine Test Hours Based on Variance Percentile
def determine_test_hours_using_gamma(variance, gamma_params):
    shape, loc, scale = gamma_params
    percentile = gamma.cdf(variance, shape, loc=loc, scale=scale)  # Compute probability
    return int(np.clip(10 + 190 * percentile, 10, 200))  # Scale test hours based on percentile

# Step 3: Determine test hours using Bayesian model (higher variance -> more test time)
def determine_test_hours(variance):
    """ Bayesian-inspired function to determine test hours based on variance."""
    return int(np.clip(10 + 190 * variance, 10, 200))  # Scaling factor for testing time

# Assign stress test hours for the selected 3 machines
test_hours_for_selected = [determine_test_hours_using_gamma(v, (shape, loc, scale)) for v in selected_variances]

# Assign stress test hours for the selected 3 machines w/o gama
test_hours_for_selected_basic = [determine_test_hours(v) for v in selected_variances]

# 5. Plot the Variance Distribution of All 30 Machines
x = np.linspace(min(mean_variance), max(mean_variance), 100)
plt.hist(mean_variance, bins=10, density=True, alpha=0.6, color='b', label="Variance of All Machines")
plt.plot(x, gamma.pdf(x, shape, loc=loc, scale=scale), 'r-', label="Fitted Gamma Distribution")
plt.xlabel("Variance of All Washing Machines")
plt.ylabel("Density")
plt.title("Gamma Distribution Fit on Variance of All Machines")
plt.legend()
plt.show()

# 6. Display Results
print("\nSelected Machines (Top 3 Variances) and Their Assigned Test Hours:")
for i, (idx, v, h) in enumerate(zip(top_3_indices, selected_variances, test_hours_for_selected)):
    print(f"Machine {idx}: Variance = {v:.2f}, Test Hours = {h}")

# 6. Display Results
print("\nSelected Machines (Top 3 Variances) and Their Assigned Test Hours:")
for i, (idx, v, h) in enumerate(zip(top_3_indices, selected_variances, test_hours_for_selected_basic)):
    print(f"Machine {idx}: Variance = {v:.2f}, Test Hours = {h}")
