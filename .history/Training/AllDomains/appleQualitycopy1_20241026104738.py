import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Load the dataset
file_path = r'C:\Users\srira\OneDrive\Desktop\Gen_AI\Training\AllDomains\apple_quality.csv' # Update this path
data = pd.read_csv(file_path)

# Display the first few rows of the dataset
print("First few rows of the dataset:")
print(data.head())

print(data.info())

# Display basic statistics
print("\nBasic statistics:")
print(data.describe())

# Check for missing values
print("\nMissing values in each column:")
print(data.isnull().sum())

# Visualize distributions of specific numeric features
features_of_interest = ['Size', 'Weight', 'Sweetness', 'Crunchiness', 'Juiciness', 'Ripeness', 'Acidity']
numeric_data = data[features_of_interest]

plt.figure(figsize=(12, 6))
for i, column in enumerate(numeric_data.columns):
    plt.subplot(2, (len(numeric_data.columns) + 1) // 2, i + 1)
    sns.histplot(numeric_data[column], kde=True)
    plt.title(f'Distribution of {column}')
plt.tight_layout()
plt.show()
