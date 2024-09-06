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

# Prior probability of being sick
p_S = 0.5  # Initial probability of having the disease
true_state = np.random.rand() < p_S  # Simulate if the patient is sick

# Sensitivity and specificity
sensitivity = 0.97  # Sensitivity of the test (true positive rate)
specificity = 0.999  # Specificity of the test (true negative rate)

# Calculating the false positive and false negative rates
false_positive_rate = 1 - specificity
false_negative_rate = 1 - sensitivity

# Simulate test results based on the true state
test_results = []
for _ in range(10):  # Simulate 3 test results
    if true_state:  # Patient is truly sick
        test_result = np.random.rand() > false_negative_rate  # Test positive with probability 1 - false negative rate
    else:  # Patient is not sick
        test_result = np.random.rand() < false_positive_rate  # Test positive with probability = false positive rate

    test_results.append("positive" if test_result else "negative")

# Store the probabilities after each test
posterior_probabilities = [p_S]

# Iterate over the test results and update the probability
for result in test_results:
    p_S = bayes_update(p_S, sensitivity, specificity, result)
    posterior_probabilities.append(p_S)

# Plotting the results
plt.plot(range(len(posterior_probabilities)), posterior_probabilities, marker='o', linestyle='-', color='b')
plt.title('Posterior Probability')
plt.text(0.5, -0.2, f'Initial probability {p_S}, \n false_positive_rate = {false_positive_rate}, \n false_negative_rate = {false_negative_rate}',
         ha='center', va='center', transform=plt.gca().transAxes)
plt.xlabel('Test Number')
plt.ylabel('Posterior Probability of Having Disease')
plt.xticks(range(len(posterior_probabilities)))
plt.grid(True)
plt.subplots_adjust(bottom=0.2)  # Adjust the bottom margin to make space for the note
plt.show()

# Display the simulated true state and test results
print(f"True state (sick): {true_state}")
print(f"Test results: {test_results}")

