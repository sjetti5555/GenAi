# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, ttest_ind
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import networkx as nx

# 1. Introduction: Data Generation for Andhra Pradesh Industry Analysis
np.random.seed(42)
industries = ['Manufacturing', 'IT', 'Renewable Energy', 'Pharmaceuticals', 'Textiles']
data = pd.DataFrame({
    'Industry': np.random.choice(industries, 100),
    'Investment': np.random.uniform(10, 500, 100),  # Investment in Crores
    'Employment': np.random.randint(50, 5000, 100),
    'Growth_Rate': np.random.uniform(2, 15, 100)  # Annual Growth Rate in %
})
print(data.head())

# 2. Role of Mathematics: Linear Regression Example
X = data[['Investment']]
y = data['Growth_Rate']
model = LinearRegression()
model.fit(X, y)
print(f"Linear Regression Coefficient: {model.coef_}, Intercept: {model.intercept_}")

# 3. Module 1 & 2: Probability and Random Variables
prob_distribution = norm.rvs(size=1000, loc=5, scale=2)
sns.histplot(prob_distribution, kde=True)
plt.title('Probability Distribution of Economic Indicator')
plt.show()

# 4. Module 3: Descriptive Statistics
print(f"Mean Investment: {data['Investment'].mean()}")
print(f"Median Employment: {data['Employment'].median()}")
print(f"Mode of Industries: {data['Industry'].mode()}")

# 5. Modules 4, 5, & 6: Linear Algebra Concepts
A = np.array([[1, 2], [3, 4]])
B = np.array([10, 20])
solution = np.linalg.solve(A, B)
print(f"Solution to the system of linear equations: {solution}")

# 6. Module 8: Social Networks & Random Graphs
G = nx.erdos_renyi_graph(n=5, p=0.6)
nx.draw(G, with_labels=True)
plt.title('Industry Network Graph')
plt.show()

# 7. Python for Data Analysis: Overview of Libraries
print("Libraries like NumPy and Pandas are used for efficient data handling.")

# 8. Modules 5 & 6: NumPy and Pandas Operations
data['Investment_Squared'] = np.square(data['Investment'])
print(data.head())

# 9. Module 7: Data Visualization Using Matplotlib and Seaborn
plt.figure(figsize=(8, 5))
sns.scatterplot(data=data, x='Investment', y='Growth_Rate', hue='Industry')
plt.title('Investment vs Growth Rate by Industry')
plt.show()

# 10. Python Statistics for Data Science: T-test Example
group1 = data[data['Industry'] == 'Manufacturing']['Growth_Rate']
group2 = data[data['Industry'] == 'IT']['Growth_Rate']
t_stat, p_value = ttest_ind(group1, group2)
print(f"T-test results: T-statistic = {t_stat}, P-value = {p_value}")

# 11. Regression and Clustering
kmeans = KMeans(n_clusters=3)
data['Cluster'] = kmeans.fit_predict(data[['Investment', 'Growth_Rate']])
sns.scatterplot(data=data, x='Investment', y='Growth_Rate', hue='Cluster')
plt.title('Cluster Analysis of Industries')
plt.show()

# 12. Conclusion & Future Directions
print("Data-driven analysis aids in targeted policies, driving industrial growth in Andhra Pradesh.")
