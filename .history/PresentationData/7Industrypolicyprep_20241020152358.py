import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, ttest_ind
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import scipy.stats as stats

# Step 1: Load Dataset from CSV
file_path = r'C:\Users\srira\OneDrive\Desktop\Gen_AI\PresentationData\industry_data.csv'
df = pd.read_csv(file_path)

# Display the first few rows of the DataFrame to verify the data
print("Loaded Dataset:")
# Convert Annual_Output to integers for better readability
df['Annual_Output'] = df['Annual_Output'].astype(int)
print(df.head())

# Check for missing values
if df.isnull().values.any():
    print("Warning: Missing values found in the dataset.")

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
plt.xlabel("Value")
plt.ylabel("Density")
plt.show()

# Step 4: Confidence Interval Calculation
std_dev = df['Workforce_Size'].std()
confidence_level = 0.95
n = len(df)
h = stats.norm.ppf((1 + confidence_level) / 2) * (std_dev / np.sqrt(n))
confidence_interval = (mean_workforce - h, mean_workforce + h)

# Convert confidence interval to standard Python floats for cleaner output
confidence_interval = (float(confidence_interval[0]), float(confidence_interval[1]))

# Step 5: Clustering Analysis
kmeans = KMeans(n_clusters=3)
df['Cluster'] = kmeans.fit_predict(df[['Workforce_Size', 'Annual_Output']])
sns.scatterplot(data=df, x='Workforce_Size', y='Annual_Output', hue='Cluster', palette='viridis')
plt.title('Industry Clusters Based on Workforce Size and Annual Output')
plt.xlabel('Workforce Size')
plt.ylabel('Annual Output')
plt.show()

# Step 6: T-Test
group1 = df[df['Industry_Type'] == 'Manufacturing']['Annual_Output']
group2 = df[df['Industry_Type'] == 'Agriculture']['Annual_Output']

# Check if groups are not empty before performing T-Test
if len(group1) > 0 and len(group2) > 0:
    t_stat, p_value = ttest_ind(group1, group2)
else:
    t_stat, p_value = None, None
    print("Warning: One of the groups for the T-Test is empty.")

# Step 7: Linear Regression
X = df[['Workforce_Size']].values
y = df['Annual_Output'].values
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)
plt.scatter(X, y, color='blue', label='Actual')
plt.plot(X, y_pred, color='red', label='Predicted')
plt.title('Regression Model: Workforce Size vs Annual Output')
plt.xlabel('Workforce Size')
plt.ylabel('Annual Output')
plt.legend()
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

# Print summary results
print("\nSummary Results:")
for key, value in summary.items():
    print(f"{key}: {value}")
