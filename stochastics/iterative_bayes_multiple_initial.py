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

# Sensitivity and specificity
sensitivity = 0.97  # Sensitivity of the test (true positive rate)
specificity = 0.999  # Specificity of the test (true negative rate)

# Calculate the false positive and false negative rates
false_positive_rate = 1 - specificity
false_negative_rate = 1 - sensitivity

# Simulation parameters
num_tests = 10  # Number of tests to simulate
initial_probabilities = np.linspace(0.1, 0.9, 10) # List of different initial probabilities

# Create a figure for plotting
plt.figure(figsize=(12, 8))

# Iterate over each initial probability
for initial_p_S in initial_probabilities:
    p_S = initial_p_S
    true_state = np.random.rand() < p_S  # Simulate if the patient is sick

    # Simulate test results based on the true state
    test_results = []
    for _ in range(num_tests):
        if true_state:  # Patient is truly sick
            test_result = np.random.rand() > false_negative_rate  # Test positive with probability 1 - false negative rate
        else:  # Patient is not sick
            test_result = np.random.rand() < false_positive_rate  # Test positive with probability = false positive rate
        test_result=True
        test_results.append("positive" if test_result else "negative")

    # Store the probabilities after each test
    posterior_probabilities = [initial_p_S]

    # Iterate over the test results and update the probability
    for result in test_results:
        p_S = bayes_update(p_S, sensitivity, specificity, result)
        posterior_probabilities.append(p_S)

    # Plotting the results for the current initial probability
    plt.plot(range(len(posterior_probabilities)), posterior_probabilities, marker='o', linestyle='-', label=f'Initial probability {initial_p_S}')

# Add plot details
plt.title('Posterior Probability vs. Number of Tests')
plt.xlabel('Test Number')
plt.ylabel('Posterior Probability of Having Disease')
plt.xticks(range(num_tests + 1))
plt.legend()  # Add legend to the plot
plt.grid(True)
plt.show()

# Display the simulated test results
for p_S in initial_probabilities:
    true_state = np.random.rand() < p_S  # Simulate if the patient is sick
    test_results = []
    for _ in range(num_tests):
        if true_state:  # Patient is truly sick
            test_result = np.random.rand() > false_negative_rate
        else:  # Patient is not sick
            test_result = np.random.rand() < false_positive_rate

        test_results.append("positive" if test_result else "negative")

    print(f"Initial probability {p_S} - True state (sick): {true_state}")
    print(f"Test results: {test_results}")
    print()

