import numpy as np
from scipy.stats import beta

# Assume prior knowledge about failure rates (Beta distribution)
alpha_prior, beta_prior = 2, 5  # Weak belief that most machines are reliable

# Observed failures from previous testing phases
failures = np.array([3, 7, 10])  # Failures per test case
tests = np.array([20, 20, 20])   # Total tests per machine

# Bayesian update: Posterior distribution of failure rates
alpha_post = alpha_prior + failures
beta_post = beta_prior + (tests - failures)

# Use Thompson Sampling to decide test hours for new machines
sampled_failure_probs = beta.rvs(alpha_post, beta_post)

# Assign test hours based on sampled failure probability
max_hours = 100
test_hours = sampled_failure_probs * max_hours

print(f"Test hours assigned to each machine: {test_hours}")

