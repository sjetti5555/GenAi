import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Step 1: Load and Explore the Dataset
file_path = r'C:\Users\srira\OneDrive\Desktop\Gen_AI\Training\AllDomains\1IndustrialPolicyDataset.py.csv'
df = pd.read_csv(file_path)

# Display initial rows, descriptive statistics, info, and null values
print("First five rows of the dataset:\n", df.head())
print("\nDescriptive statistics:\n", df.describe())
print("\nDataset information:\n", df.info())
print("\nNull values in each column:\n", df.isnull().sum())

# Step 2: Handling Null Values
# Fill numerical null values with the median value
df['Employment'].fillna(df['Employment'].median(), inplace=True)
df['Investment'].fillna(df['Investment'].median(), inplace=True)

# Step 3: Detect and Handle Outliers using Box Plot
# Plot box plots for numerical columns to detect outliers
numerical_cols = ['Employment', 'Investment', 'Growth Rate (%)', 'Exports', 'Revenue']
plt.figure(figsize=(15, 10))
for i, col in enumerate(numerical_cols, 1):
    plt.subplot(2, 3, i)
    sns.boxplot(y=col, data=df)
    plt.title(f'Box Plot - {col}')
plt.tight_layout()
plt.show()

# Capping outliers within the 5th and 95th percentiles
for col in numerical_cols:
    upper_limit = df[col].quantile(0.95)
    lower_limit = df[col].quantile(0.05)
    df[col] = np.where(df[col] > upper_limit, upper_limit, np.where(df[col] < lower_limit, lower_limit, df[col]))

print("\nOutliers handled with capping method.")

# Step 4: Heatmap for Correlation Analysis
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Heatmap of Numerical Features")
plt.show()

# Step 5: Visualization of Numerical Data
# 1. Line plot for Growth Rate over Years
plt.figure(figsize=(12, 6))
sns.lineplot(x='Year', y='Growth Rate (%)', data=df, ci=None)
plt.title('Growth Rate Over the Years')
plt.xlabel("Year")
plt.ylabel("Growth Rate (%)")
plt.show()

# 2. Bar plot for Average Investment by Sector
plt.figure(figsize=(12, 6))
sns.barplot(x='Sector', y='Investment', data=df, estimator=np.mean, ci=None, palette='viridis')
plt.title('Average Investment by Sector')
plt.xticks(rotation=45)
plt.xlabel("Sector")
plt.ylabel("Average Investment (INR crore)")
plt.show()

# Step 6: Train and Predict with Linear Regression
# Prepare features and target for predicting Revenue based on growth and investment
X = df[['Year', 'Employment', 'Investment', 'Growth Rate (%)', 'Exports']]
y = df['Revenue']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Model evaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'\nModel Mean Squared Error: {mse}')
print(f'Model R^2 Score: {r2}')

# Visualize predictions vs actual values
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.6, color="purple")
plt.xlabel("Actual Revenue")
plt.ylabel("Predicted Revenue")
plt.title("Actual vs Predicted Revenue (Scatter Plot)")
plt.show()

# Step 7: Policy Recommendations for Backward Sectors
# Check for sectors with lower growth and investment
for sector in df['Sector'].unique():
    sector_data = df[df['Sector'] == sector]
    avg_growth = sector_data['Growth Rate (%)'].mean()
    avg_investment = sector_data['Investment'].mean()
    
    print(f"\nPolicy Recommendation for {sector} Sector:")
    if avg_growth < df['Growth Rate (%)'].mean() or avg_investment < df['Investment'].mean():
        print("   - Increase targeted investment to support growth.")
        print("   - Implement training and employment programs.")
        print("   - Adopt sustainability measures for environmental impact.")
    else:
        print("   - Maintain current investment and continue monitoring growth.")

print("\nAnalysis complete.")
