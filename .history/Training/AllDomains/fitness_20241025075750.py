import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Load the dataset
file_path = r'C:\Users\srira\OneDrive\Desktop\Gen_AI\Training\AllDomains\mturkfitbit_export_3.12.16-4.11.16\Fitabase Data 3.12.16-4.11.16\dailyActivity_merged.csv' # Update this path
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

# Ask user how to handle null values
handle_nulls = input("Do you want to handle null values? (yes/no): ").strip().lower()

if handle_nulls == 'yes':
    method = input("Choose a method to handle null values (mean/median/mode/drop): ").strip().lower()
    if method in ['mean', 'median', 'mode']:
        # Handle missing values based on user choice
        if method == 'mean':
            data.fillna(data.mean(), inplace=True)
        elif method == 'median':
            data.fillna(data.median(), inplace=True)
        elif method == 'mode':
            for column in data.select_dtypes(include=[np.object]).columns:
                data[column].fillna(data[column].mode()[0], inplace=True)
            for column in data.select_dtypes(include=[np.number]).columns:
                data[column].fillna(data[column].mode()[0], inplace=True)
    elif method == 'drop':
        data.dropna(inplace=True)
    else:
        print("Invalid method selected. No changes made to null values.")

# Visualize distributions of numeric features
numeric_data = data.select_dtypes(include=['number'])
plt.figure(figsize=(12, 6))
for i, column in enumerate(numeric_data.columns):
    plt.subplot(2, (len(numeric_data.columns) + 1) // 2, i + 1)
    sns.histplot(data[column], kde=True)
    plt.title(f'Distribution of {column}')
plt.tight_layout()
plt.show()

# Draw boxplots for outliers
plt.figure(figsize=(12, 6))
for i, column in enumerate(numeric_data.columns):
    plt.subplot(2, (len(numeric_data.columns) + 1) // 2, i + 1)
    sns.boxplot(y=numeric_data[column])
    plt.title(f'Boxplot of {column}')
plt.tight_layout()
plt.show()

# Correlation heatmap
correlation_matrix = numeric_data.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Correlation Heatmap')      
plt.show()

# Data Preprocessing
# Handle missing values (example: fill with mean for numeric columns)
numeric_cols = data.select_dtypes(include=[np.number]).columns  # Select only numeric columns
data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())  # Fill missing values with mean

# Encode categorical variables if any
data = pd.get_dummies(data, drop_first=True)

# Define features and target variable
X = data.drop('TotalSteps', axis=1)  # Replace 'target_column' with the actual target variable name
y = data['TotalSteps']  # Replace 'target_column' with the actual target variable name

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

# Visualize Actual vs Predicted
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')  # Line for perfect predictions
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted')
plt.show()

# Feature Importance
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

# Visualize feature importance
plt.figure(figsize=(12, 6))
plt.title('Feature Importances')
plt.bar(range(X.shape[1]), importances[indices], align='center')
plt.xticks(range(X.shape[1]), X.columns[indices], rotation=90)
plt.xlim([-1, X.shape[1]])
plt.show()
