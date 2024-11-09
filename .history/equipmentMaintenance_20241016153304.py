from scipy.stats import beta
import matplotlib.pyplot as plt
import numpy as np

# Initial prior parameters (alpha and beta for the Beta distribution)
alpha_prior = 2  # Represents initial belief (failures)
beta_prior = 38  # Represents initial belief (successes)
prior_mean = alpha_prior / (alpha_prior + beta_prior)
print(f"Initial probability of failure: {prior_mean * 100:.2f}%")

# Function to update the prior based on observed data
def update_belief(alpha_prior, beta_prior, successes, failures):
    alpha_posterior = alpha_prior + failures
    beta_posterior = beta_prior + successes
    return alpha_posterior, beta_posterior

# Simulated data: Number of hours operated without failure
hours_data = [200, 300, 400]  # Update with each new observation (in hours)
observed_failures = [0, 0, 1]  # Corresponding failures observed (0 = no failure, 1 = failure)

# Iterate over the data to update beliefs
for i, (hours, failure) in enumerate(zip(hours_data, observed_failures)):
    if failure:
        print(f"Failure observed after {sum(hours_data[:i+1])} hours.")
    else:
        print(f"No failure observed up to {sum(hours_data[:i+1])} hours.")
    
    alpha_prior, beta_prior = update_belief(alpha_prior, beta_prior, hours, failure)
    updated_mean = alpha_prior / (alpha_prior + beta_prior)
    print(f"Updated probability of failure: {updated_mean * 100:.2f}%\n")

# Visualization: Posterior distribution
x = np.linspace(0, 1, 100)
posterior = beta.pdf(x, alpha_prior, beta_prior)

plt.figure(figsize=(8, 4))
plt.plot(x, posterior, label=f'Posterior after {sum(hours_data)} hours', color='blue')
plt.title('Posterior Distribution of Equipment Failure')
plt.xlabel('Probability of Failure')
plt.ylabel('Density')
plt.legend()
plt.grid(True)
plt.show()
