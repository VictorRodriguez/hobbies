import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

# Parameters
num_washing_machines = 30  # Total machines
test_phases = 5            # Number of testing phases
machines_per_phase = 3      # Number of machines selected per phase
max_test_hours = 100        # Maximum possible test hours per machine

# Initialize prior beliefs (Beta distribution)
alpha_prior = np.ones(num_washing_machines) * 2  # Prior successes
beta_prior = np.ones(num_washing_machines) * 5   # Prior failures

# Simulated "true" failure rates for each washing machine (unknown in real life)
true_failure_rates = np.random.uniform(0.05, 0.4, size=num_washing_machines)  # Between 5% and 40% failure probability

# Initialize tracking of test results
test_results = np.zeros(num_washing_machines)  # Failures per machine
total_tests = np.zeros(num_washing_machines)   # Total tests per machine

# Simulation loop across test phases
for phase in range(test_phases):
    print(f"\n🔍 Phase {phase+1}")

    # Compute variance per machine (proxy for uncertainty)
    variances = beta.var(alpha_prior, beta_prior)

    # Select the machines with the highest variance for testing
    selected_indices = np.argsort(variances)[-machines_per_phase:]

    print(f"Selected machines for testing: {selected_indices}")

    # Thompson Sampling: Sample from posterior to determine test hours
    sampled_failure_probs = beta.rvs(alpha_prior[selected_indices], beta_prior[selected_indices])
    test_hours = sampled_failure_probs * max_test_hours  # Scale by max test hours

    print(f"Assigned test hours: {test_hours}")

    # Simulate test execution
    for i, machine_idx in enumerate(selected_indices):
        num_tests = int(test_hours[i] / 10)  # Assume every 10 hours = 1 test cycle
        failures = np.random.binomial(num_tests, true_failure_rates[machine_idx])  # Simulate failures

        # Update observed failures and total tests
        test_results[machine_idx] += failures
        total_tests[machine_idx] += num_tests

        # Update Bayesian posterior
        alpha_prior[machine_idx] += failures
        beta_prior[machine_idx] += (num_tests - failures)

    # Visualize posterior updates
    x_vals = np.linspace(0, 0.5, 100)
    plt.figure(figsize=(10, 5))
    for idx in selected_indices:
        plt.plot(x_vals, beta.pdf(x_vals, alpha_prior[idx], beta_prior[idx]), label=f"Machine {idx}")
    plt.title(f"Phase {phase+1}: Updated Failure Rate Distributions")
    plt.xlabel("Failure Probability")
    plt.ylabel("Density")
    plt.legend()
    plt.show()

# Final test results
print("\nFinal failure rate estimates:")
for i in range(num_washing_machines):
    mean_failure_rate = alpha_prior[i] / (alpha_prior[i] + beta_prior[i])
    print(f"Machine {i}: Estimated Failure Rate = {mean_failure_rate:.3f}")

