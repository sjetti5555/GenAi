import numpy as np

# Data: Numbers from 1 to 10
data = np.arange(1, 10)

# Calculate mean
mean = np.mean(data)
print(f"Mean: {mean}")

# Calculate median
median = np.median(data)
print(f"Median: {median}")

# Calculate variance
variance = np.var(data, ddof=0)  # Population variance
print(f"Variance: {variance}")

# Calculate standard deviation
std_deviation = np.std(data, ddof=0)  # Population standard deviation
print(f"Standard Deviation: {std_deviation}")

# Calculate skewness using mean and median
skewness = (3 * (mean - median)) / std_deviation
print(f"Skewness: {skewness}")
