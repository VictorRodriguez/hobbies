import numpy as np
import matplotlib.pyplot as plt

# Function to apply Bayes' Theorem after each test
def bayes_update(prior, sensitivity, specificity, result):
    if result == "positive":
        likelihood = sensitivity
        false_alarm_rate = 1 - specificity
    else:
        likelihood = 1 - sensitivity
        false_alarm_rate = specificity

    numerator = likelihood * prior
    denominator = (likelihood * prior) + (false_alarm_rate * (1 - prior))

    posterior = numerator / denominator
    return posterior

# Parameters
p_S = 0.5  # Initial probability of having the disease
sensitivity = 0.75  # Sensitivity of the test (true positive rate)
specificity = 0.97  # Specificity of the test (true negative rate)
false_positive_rate = 1 - specificity
false_negative_rate = 1 - sensitivity

# Target probability and max test limit
target_posterior = 0.95
num_simulations = 1000  # Number of runs
max_tests_per_run = 50  # Limit the number of tests per run to avoid infinite loops

# Function to simulate a single run
def simulate_single_run():
    p_S = 0.5  # Reset prior probability for each run
    true_state = np.random.rand() < p_S  # Simulate if the patient is sick
    num_tests = 0

    if true_state:  # Patient is truly sick
        test_result = np.random.rand() > false_negative_rate  # False negative rate
    else:  # Patient is not sick
        test_result = np.random.rand() < false_positive_rate  # False positive rate

    result = "positive" if test_result else "negative"

    if result == "positive":
        target_posterior=0.95
        while p_S <= target_posterior and num_tests < max_tests_per_run:
            p_S = bayes_update(p_S, sensitivity, specificity, result)
            print(p_S)
            num_tests += 1
    else:
        target_posterior=0.05
        while p_S >= target_posterior and num_tests < max_tests_per_run:
            p_S = bayes_update(p_S, sensitivity, specificity, result)
            num_tests += 1
            print(p_S)
    return num_tests

# Simulate multiple runs
test_counts = []
for _ in range(num_simulations):
    test_counts.append(simulate_single_run())

print(test_counts)
# Calculate the average number of tests needed
average_tests = np.mean(test_counts)

# Plot the results
plt.hist(test_counts, bins=30, color='blue', alpha=0.7)
plt.axvline(average_tests, color='red', linestyle='dashed', linewidth=1)
plt.title('Distribution of Number of Tests to Reach 95% Posterior Probability')
plt.xlabel('Number of Tests')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# Display the average number of tests
print(f"Average number of tests to reach 95% posterior probability: {average_tests:.2f}")

