import numpy as np
import scipy.stats as stats

# Sample data: Daily productivity (in square meters per worker per day)
productivity_data = [14, 16, 15, 17, 16, 14, 15, 18, 14, 15, 16, 17, 16, 15, 14]

# 1. Point of Estimation: Mean of the sample
mean_productivity = np.mean(productivity_data)
print(f"Point estimate of average productivity: {mean_productivity:.2f} square meters/day")

# 2. Margin of Error
# Assuming a 95% confidence level, calculate the margin of error using t-distribution
confidence_level = 0.95
alpha = 1 - confidence_level
n = len(productivity_data)
sample_std = np.std(productivity_data, ddof=1)  # Sample standard deviation
t_critical = stats.t.ppf(1 - alpha/2, df=n-1)  # t-critical value for 95% confidence

# Margin of Error = t_critical * (sample_std / sqrt(n))
margin_of_error = t_critical * (sample_std / np.sqrt(n))
print(f"Margin of error at 95% confidence level: {margin_of_error:.2f} square meters/day")

# Confidence Interval
lower_bound = mean_productivity - margin_of_error
upper_bound = mean_productivity + margin_of_error
print(f"95% Confidence Interval: ({lower_bound:.2f}, {upper_bound:.2f}) square meters/day")

# 3. Hypothesis Testing
# Null Hypothesis (H0): The average productivity is 15 square meters/day
# Alternative Hypothesis (H1): The average productivity is not 15 square meters/day

# Define the hypothesized mean
hypothesized_mean = 15

# Perform a t-test
t_statistic, p_value = stats.ttest_1samp(productivity_data, hypothesized_mean)

print(f"T-statistic: {t_statistic:.2f}")
print(f"P-value: {p_value:.4f}")

# Decision based on p-value
if p_value < alpha:
    print("Reject the null hypothesis: The average productivity is significantly different from 15 square meters/day.")
else:
    print("Fail to reject the null hypothesis: There is no significant difference from 15 square meters/day.")
