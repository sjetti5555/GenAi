
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Generate random data from a normal distribution
data = np.random.normal(50, 5, 1000)

# Calculate statistics
mean = np.mean(data)
median = np.median(data)


std_deviation = np.std(data, ddof=0)  # Population standard deviation
variance = np.var(data, ddof=0)  # Population variance

# Print the calculated statistics
print(f"Mean: {mean:.2f}")
print(f"Median: {median:.2f}")

print(f"Standard Deviation: {std_deviation:.2f}")
print(f"Variance: {variance:.2f}")

# Plotting the normal distribution curve
plt.figure(figsize=(10, 6))

# Plot histogram
sns.histplot(data, bins=30, kde=True, color='blue', stat='density', alpha=0.6)

# Plot the normal distribution curve
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = stats.norm.pdf(x, mean, std_deviation)
plt.plot(x, p, 'k', linewidth=2)

# Add titles and labels
plt.title('Normal Distribution Curve')
plt.xlabel('Value')
plt.ylabel('Density')

# Show the plot
plt.show()
