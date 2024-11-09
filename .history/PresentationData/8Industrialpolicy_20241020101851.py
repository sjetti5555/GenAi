# Re-import necessary libraries after reset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, classification_report, confusion_matrix
import statsmodels.api as sm
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

# Generate random dataset for industrial data analysis
np.random.seed(42)
data = pd.DataFrame({
    'Industry': np.random.choice(['Manufacturing', 'IT', 'Agriculture', 'Textiles', 'Pharmaceuticals'], size=200),
    'Annual_Output': np.random.randint(10000, 100000, size=200),
    'Workforce_Size': np.random.randint(50, 500, size=200),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], size=200),
    'Investments': np.random.uniform(5000, 50000, size=200),
    'Growth_Rate': np.random.normal(loc=5, scale=2, size=200)
})

# Save the dataset to CSV for user download
data.to_csv("C:/Users/srira/OneDrive/Desktop/Gen_AI/PresentationData/1industrial_data.csv", index=False)

# 1. Descriptive Analysis
mean_output = data['Annual_Output'].mean()
median_output = data['Annual_Output'].median()
mode_industry = data['Industry'].mode()[0]
std_dev_output = data['Annual_Output'].std()

# Visualize the distribution of Annual Output
plt.figure(figsize=(8, 5))
sns.histplot(data['Annual_Output'], kde=True)
plt.title('Distribution of Annual Output')
plt.xlabel('Annual Output')
plt.ylabel('Frequency')
plt.show()

# 2. Probability Analysis - Normal Distribution
plt.figure(figsize=(8, 5))
sns.histplot(data['Growth_Rate'], kde=True, bins=20)
plt.title('Growth Rate Distribution (Normal Distribution)')
plt.xlabel('Growth Rate')
plt.ylabel('Frequency')
plt.show()

# Calculate probability of growth rate being above 6%
prob_above_6 = 1 - stats.norm.cdf(6, loc=data['Growth_Rate'].mean(), scale=data['Growth_Rate'].std())

# 3. Statistical Inference - Hypothesis Testing
# Hypothesis: Mean annual output of Manufacturing industry is greater than 60,000
manufacturing_data = data[data['Industry'] == 'Manufacturing']['Annual_Output']
t_stat, p_value = stats.ttest_1samp(manufacturing_data, 60000)

# 4. Clustering - K-means Clustering for Investment Analysis
kmeans = KMeans(n_clusters=3)
data['Investment_Cluster'] = kmeans.fit_predict(data[['Investments']])

# Visualize Clustering
plt.figure(figsize=(8, 5))
sns.scatterplot(data=data, x='Investments', y='Annual_Output', hue='Investment_Cluster', palette='viridis')
plt.title('Investment Clustering Analysis')
plt.xlabel('Investments')
plt.ylabel('Annual Output')
plt.show()

# 5. Regression Modeling - Linear Regression
X = data[['Workforce_Size', 'Investments']]
y = data['Annual_Output']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Linear Regression model
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)

# Predict and visualize
y_pred = lin_reg.predict(X_test)
plt.figure(figsize=(8, 5))
plt.scatter(y_test, y_pred)
plt.plot(y_test, y_test, color='red')
plt.title('Actual vs Predicted Annual Output')
plt.xlabel('Actual Annual Output')
plt.ylabel('Predicted Annual Output')
plt.show()

# 6. Logistic Regression - Binary Classification (High vs. Low Growth)
data['High_Growth'] = (data['Growth_Rate'] > 6).astype(int)
X = data[['Workforce_Size', 'Investments']]
y = data['High_Growth']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)
y_pred_log = log_reg.predict(X_test)

# Classification report
classification_rep = classification_report(y_test, y_pred_log)

# Display results
{
    "Mean Annual Output": mean_output,
    "Median Annual Output": median_output,
    "Mode of Industry": mode_industry,
    "Standard Deviation of Output": std_dev_output,
    "Probability of Growth Rate > 6%": prob_above_6,
    "T-Statistic for Manufacturing Output": t_stat,
    "P-Value for Manufacturing Output": p_value,
    "Linear Regression Coefficients": lin_reg.coef_,
    "Logistic Regression Classification Report": classification_rep
}

# Step 1: Generate a synthetic dataset
X, y = make_classification(n_samples=1000, n_features=20, n_classes=3, n_informative=10, n_redundant=5, random_state=42)

# Step 2: Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Train a Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Step 4: Make predictions
y_pred = model.predict(X_test)

# Step 5: Evaluate the model
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
# Use zero_division parameter to avoid UndefinedMetricWarning
report = classification_report(y_test, y_pred, zero_division=1)
print(report)
