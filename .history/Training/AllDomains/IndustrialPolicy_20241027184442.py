import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
file_path = r'C:\Users\srira\OneDrive\Desktop\Gen_AI\Training\AllDomains\1IndustrialPolicyDataset.py.csv'
df = pd.read_csv(file_path)
print(df.head())
print(df.describe())
print(df.info())

# Step 1: Data Cleaning
# Fill missing values with median (for numerical columns)
df['Employment'].fillna(df['Employment'].median(), inplace=True)
df['Investment'].fillna(df['Investment'].median(), inplace=True)

# Detect and remove duplicates
df.drop_duplicates(inplace=True)

# Capping outliers in 'Growth Rate (%)' within the 5th and 95th percentiles
upper_limit = df['Growth Rate (%)'].quantile(0.95)
lower_limit = df['Growth Rate (%)'].quantile(0.05)
df['Growth Rate (%)'] = np.where(df['Growth Rate (%)'] > upper_limit, upper_limit,
                                 np.where(df['Growth Rate (%)'] < lower_limit, lower_limit, df['Growth Rate (%)']))

print("Data cleaning complete.")

# Step 2: Descriptive Statistics and Data Visualization
print("Descriptive statistics:\n", df.describe())

# 1. Investment by Sector
plt.figure(figsize=(10, 6))
sns.boxplot(x='Sector', y='Investment', data=df)
plt.title('Investment Distribution by Sector')
plt.xticks(rotation=45)
plt.show()

# 2. Employment by Year
plt.figure(figsize=(10, 6))
sns.lineplot(x='Year', y='Employment', data=df, estimator='mean')
plt.title('Average Employment over the Years')
plt.show()

# 3. Revenue by Growth Rate
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Growth Rate (%)', y='Revenue', data=df, hue='Sector')
plt.title('Revenue vs Growth Rate by Sector')
plt.show()

# Step 3: Modeling for Future Predictions
# Prepare features and target
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
print(f'Model Mean Squared Error: {mse}')
print(f'Model R^2 Score: {r2}')

# Visualize predictions vs actual values
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.6)
plt.xlabel("Actual Revenue")
plt.ylabel("Predicted Revenue")
plt.title("Actual vs Predicted Revenue")
plt.show()

# Policy Recommendations (For reference, as the code output is for analysis)
print("Policy Recommendations based on the analysis:")
print("1. Increase investment in sectors with high growth rate but lower revenue to stimulate growth.")
print("2. Enhance employment programs in sectors with steady growth but low workforce.")
print("3. Implement sustainability measures in sectors with high environmental impact.")
