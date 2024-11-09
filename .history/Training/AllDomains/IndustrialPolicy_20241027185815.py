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
print(df.isnull().sum())






# Step 2: Descriptive Statistics and Visualization for Each Sector Separately

# List of unique sectors in the dataset
sectors = df['Sector'].unique()

for sector in sectors:
    sector_data = df[df['Sector'] == sector]
    
    # Plot 1: Investment Trend over the Years using a Bar Plot for each sector
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Year', y='Investment', data=sector_data, ci=None, palette='viridis')
    plt.title(f'Investment Over Years - {sector} Sector (Bar Plot)')
    plt.xlabel("Year")
    plt.ylabel("Investment (INR crore)")
    plt.show()

    # Plot 2: Employment over the Years using a Point Plot for each sector
    plt.figure(figsize=(12, 6))
    sns.pointplot(x='Year', y='Employment', data=sector_data, ci=None, color='blue', markers="o")
    plt.title(f'Employment Over Years - {sector} Sector (Point Plot)')
    plt.xlabel("Year")
    plt.ylabel("Employment")
    plt.show()

    # Plot 3: Revenue vs Growth Rate with a Regression Plot for each sector
    plt.figure(figsize=(12, 6))
    sns.regplot(x='Growth Rate (%)', y='Revenue', data=sector_data, scatter_kws={'alpha':0.6}, line_kws={"color": "red"})
    plt.title(f'Revenue vs Growth Rate - {sector} Sector (Regression Plot)')
    plt.xlabel("Growth Rate (%)")
    plt.ylabel("Revenue (INR crore)")
    plt.show()

print("Sector-specific visualizations complete.")

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
plt.scatter(y_test, y_pred, alpha=0.6, color="purple")
plt.xlabel("Actual Revenue")
plt.ylabel("Predicted Revenue")
plt.title("Actual vs Predicted Revenue (Scatter Plot)")
plt.show()

# Policy Recommendations based on Analysis
print("Policy Recommendations based on the analysis:")
print("1. Increase investment in sectors with high growth rate but lower revenue to stimulate growth.")
print("2. Enhance employment programs in sectors with steady growth but low workforce.")
print("3. Implement sustainability measures in sectors with high environmental impact.")
