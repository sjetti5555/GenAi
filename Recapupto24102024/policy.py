import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress
from sklearn.cluster import KMeans

# Load industrial data (example data)
data = pd.DataFrame({
    'region': ['Region A', 'Region B', 'Region C', 'Region D'],
    'investment': [100, 200, 150, 300],
    'output': [120, 250, 180, 350],
    'employment': [500, 800, 600, 900]
})

# Descriptive statistics
print(data.describe())

# Linear regression between investment and output
slope, intercept, r_value, p_value, std_err = linregress(data['investment'], data['output'])
print(f"Linear Regression: output = {slope} * investment + {intercept}")

# Predict output for a new investment
new_investment = 250
predicted_output = slope * new_investment + intercept
print(f"Predicted output for investment {new_investment}: {predicted_output}")

# Clustering regions based on employment and output
kmeans = KMeans(n_clusters=2)
data['cluster'] = kmeans.fit_predict(data[['employment', 'output']])
sns.scatterplot(data=data, x='employment', y='output', hue='cluster')
plt.title('Clustered Regions by Employment and Output')
plt.show()

# Visualize investment vs output
plt.figure(figsize=(8, 5))
sns.regplot(x='investment', y='output', data=data)
plt.title('Investment vs Output')
plt.xlabel('Investment (in million $)')
plt.ylabel('Output (in million $)')
plt.show()
