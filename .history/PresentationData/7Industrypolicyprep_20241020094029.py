import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, ttest_ind
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import scipy.stats as stats

# Step 1: Generate Random Dataset
data = {
    "Industry_Type": np.random.choice(['Manufacturing', 'IT', 'Agriculture'], 100),
    "Workforce_Size": np.random.randint(50, 1000, size=100),
    "Annual_Output": np.random.uniform(100000, 5000000, size=100)
}
df = pd.DataFrame(data)
df.to_csv('/mnt/data/industry_data.csv', index=False)

# Step 2: Descriptive Statistics (Mean, Median, Mode)
mean_workforce = df['Workforce_Size'].mean()
median_workforce = df['Workforce_Size'].median()
mode_industry = df['Industry_Type'].mode()[0]

# Step 3: Probability Analysis with Normal Distribution
data = norm.rvs(size=1000, loc=0, scale=1)
plt.hist(data, bins=30, density=True, alpha=0.6, color='g')
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x)
plt.plot(x, p, 'k', linewidth=2)
plt.title("Normal Distribution Curve")
plt.show()

# Step 4: Confidence Interval Calculation
std_dev = df['Workforce_Size'].std()
confidence_level = 0.95
n = len(df)
h = stats.norm.ppf((1 + confidence_level) / 2) * (std_dev / np.sqrt(n))
confidence_interval = (mean_workforce - h, mean_workforce + h)

# Step 5: Clustering Analysis
kmeans = KMeans(n_clusters=3)
df['Cluster'] = kmeans.fit_predict(df[['Workforce_Size', 'Annual_Output']])
sns.scatterplot(data=df, x='Workforce_Size', y='Annual_Output', hue='Cluster')
plt.title('Industry Clusters')
plt.show()

# Step 6: T-Test
group1 = df[df['Industry_Type'] == 'Manufacturing']['Annual_Output']
group2 = df[df['Industry_Type'] == 'IT']['Annual_Output']
t_stat, p_value = ttest_ind(group1, group2)

# Step 7: Linear Regression
X = df[['Workforce_Size']].values
y = df['Annual_Output'].values
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)
plt.scatter(X, y, color='blue')
plt.plot(X, y_pred, color='red')
plt.title('Regression Model: Workforce Size vs Annual Output')
plt.xlabel('Workforce Size')
plt.ylabel('Annual Output')
plt.show()

# Output Summary
summary = {
    "Mean Workforce Size": mean_workforce,
    "Median Workforce Size": median_workforce,
    "Mode Industry Type": mode_industry,
    "Confidence Interval": confidence_interval,
    "T-Statistic": t_stat,
    "P-Value": p_value
}
summary
