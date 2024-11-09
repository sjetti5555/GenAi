# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from scipy import stats
from scipy.stats import chi2_contingency
from sklearn.model_selection import train_test_split
import sqlite3
import geopandas as gpd

# Sample Data: Industrial Policy Data for Andhra Pradesh
data = {
    "Region": ["Region_A", "Region_B", "Region_C", "Region_D", "Region_E"],
    "Policy_Investment": [50000, 75000, 60000, 90000, 80000],
    "Employment_Growth": [5.5, 6.7, 5.9, 7.8, 6.5],
    "Industrial_Output": [200000, 250000, 220000, 300000, 280000]
}

# Create a DataFrame
df = pd.DataFrame(data)
print("Data Overview:\n", df)

# Load the Andhra Pradesh map
map_df = gpd.read_file('path/to/andhra_pradesh.shp')  # Update with your shapefile path

# Define random cities in Andhra Pradesh with their coordinates
cities = {
    "Visakhapatnam": (17.6889, 83.2185),
    "Vijayawada": (16.5062, 80.6480),
    "Guntur": (16.3065, 80.4366),
    "Nellore": (14.4428, 79.9860),
    "Tirupati": (13.6288, 79.4192)
}

# Module 1: Descriptive Statistics
mean_growth = np.mean(df["Employment_Growth"])
median_growth = np.median(df["Employment_Growth"])
mode_growth = stats.mode(df["Employment_Growth"]).mode  # Removed [0]
print(f"Mean Growth: {mean_growth}, Median Growth: {median_growth}, Mode Growth: {mode_growth}")

# Module 2: Probability and Bayesian Inference
# Prior Probability: Probability of high growth with investment
prior = 0.6
likelihood = 0.75  # Likelihood of high growth given investment
evidence = 0.7   # Evidence probability

posterior = (likelihood * prior) / evidence
print(f"Posterior Probability of high growth given investment: {posterior}")

# Module 3: Statistical Inference - Hypothesis Testing
# Testing if policy investment significantly improves employment growth
# Null Hypothesis: Policy investment does not affect employment growth
# Alternative Hypothesis: Policy investment affects employment growth
t_statistic, p_value = stats.ttest_ind(df["Policy_Investment"], df["Employment_Growth"])
print(f"T-statistic: {t_statistic}, P-value: {p_value}")

if p_value < 0.05:
    print("Reject the null hypothesis: Policy investment significantly affects employment growth.")
else:
    print("Fail to reject the null hypothesis: No significant effect of investment on growth.")

# Module 4: Clustering Techniques - K-Means Clustering
# Clustering regions based on Policy Investment and Industrial Output
X = df[['Policy_Investment', 'Industrial_Output']]
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
df['Cluster'] = kmeans.labels_

print("\nClustered Data:\n", df)

# Visualize Clustering
plt.figure(figsize=(8, 6))
sns.scatterplot(x='Policy_Investment', y='Industrial_Output', hue='Cluster', data=df, palette='viridis')
plt.title('K-means Clustering of Regions Based on Investment and Industrial Output')
plt.xlabel('Policy Investment (INR)')
plt.ylabel('Industrial Output (INR)')
plt.grid(True)
plt.show()

# Module 5: Regression Modeling - Linear Regression
# Model the relationship between Policy Investment and Employment Growth
X = df[['Policy_Investment']]
y = df['Employment_Growth']
model = LinearRegression().fit(X, y)

print(f"Intercept: {model.intercept_}, Slope: {model.coef_[0]}")
predicted_growth = model.predict(pd.DataFrame([[85000]], columns=['Policy_Investment']))  # Changed to DataFrame
print(f"Predicted Employment Growth for an investment of INR 85000: {predicted_growth[0]:.2f}")

# Residual Analysis
residuals = y - model.predict(X)
sns.histplot(residuals, kde=True)
plt.title('Residual Analysis')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# Module 6: Chi-Square Testing for Categorical Data
# Example: Is there a relationship between investment categories (Low, High) and high growth?
df['Investment_Category'] = np.where(df['Policy_Investment'] > 70000, 'High', 'Low')
contingency_table = pd.crosstab(df['Investment_Category'], df['Employment_Growth'] > 6)
chi2, p, dof, expected = chi2_contingency(contingency_table)
print(f"Chi-Square Test p-value: {p}")

# Module 7: Database Integration
# Create SQLite database and store the dataframe
conn = sqlite3.connect('industrial_policy.db')
df.to_sql('policy_data', conn, if_exists='replace', index=False)
query_result = pd.read_sql('SELECT * FROM policy_data', conn)
print("Data from SQLite Database:\n", query_result)
conn.close()

# Module 8: Data Visualization
plt.figure(figsize=(15, 8))

# Plot Andhra Pradesh map
ax = map_df.plot(color='lightgrey', edgecolor='black')

# Plot major industrial areas on the map
for city, coord in cities.items():
    plt.plot(coord[1], coord[0], marker='o', color='red', markersize=8)
    plt.text(coord[1], coord[0], city, fontsize=9, ha='right')

plt.title('Map of Andhra Pradesh with Major Cities')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.grid(True)
plt.show()

# Additional Visualization: Policy Investment vs Employment Growth
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="Policy_Investment", y="Employment_Growth", hue="Cluster", palette='coolwarm')
plt.plot(X, model.predict(X), color='red', label='Regression Line')
plt.title('Policy Investment vs Employment Growth with Regression Line')
plt.xlabel('Policy Investment (INR)')
plt.ylabel('Employment Growth (%)')
plt.legend()
plt.grid(True)
plt.show()
