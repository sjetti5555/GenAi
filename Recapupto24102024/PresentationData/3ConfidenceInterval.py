import scipy.stats as stats

# Confidence interval for workforce size
mean = df['Workforce_Size'].mean()
std_dev = df['Workforce_Size'].std()
confidence_level = 0.95
n = len(df)

# Calculate confidence margin
h = stats.norm.ppf((1 + confidence_level) / 2) * (std_dev / np.sqrt(n))
print(f"Confidence Interval: {mean - h} to {mean + h}")
