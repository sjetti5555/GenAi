import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, confusion_matrix
from sklearn.cluster import KMeans
import numpy as np

# Load the dataset
file_path = r'C:\Users\srira\OneDrive\Desktop\Gen_AI\Training\AllDomains\Student_performance_data _.csv'  # Update this path
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

# Automatically handle non-numeric columns
# Convert non-numeric columns to numeric using one-hot encoding
data = pd.get_dummies(data, drop_first=True)

# Ask user how to handle missing values
handle_nulls = input("Do you want to handle missing values? (yes/no): ").strip().lower()

if handle_nulls == 'yes':
    method = input("Choose a method to handle null values (mean/median/mode/drop): ").strip().lower()
    if method in ['mean', 'median', 'mode']:
        # Handle missing values based on user choice
        if method == 'mean':
            data.fillna(data.mean(), inplace=True)
        elif method == 'median':
            data.fillna(data.median(), inplace=True)
        elif method == 'mode':
            for column in data.select_dtypes(include=['object']).columns:
                data[column].fillna(data[column].mode()[0], inplace=True)
            for column in data.select_dtypes(include=[np.number]).columns:
                data[column].fillna(data[column].mode()[0], inplace=True)
    elif method == 'drop':
        data.dropna(inplace=True)
    else:
        print("Invalid method selected. No changes made to null values.")

# Fill missing values for numeric columns with mean (if not handled by user)
numeric_cols = data.select_dtypes(include=[np.number]).columns
data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())

# Fill missing values for categorical columns with mode (if not handled by user)
categorical_cols = data.select_dtypes(include=['object']).columns
for column in categorical_cols:
    data[column].fillna(data[column].mode()[0], inplace=True)

# Print mean, median, and mode after handling null values
print("\nMean, Median, and Mode after handling null values:")
for column in numeric_cols:
    mean = data[column].mean()
    median = data[column].median()
    mode = data[column].mode()[0]  # mode() returns a Series, take the first value
    print(f"{column} - Mean: {mean}, Median: {median}, Mode: {mode}")

# Focus on specific features impacting GPA
features_of_interest = ['ParentalEducation', 'StudyTimeWeekly', 'Absences', 
                        'Tutoring', 'ParentalSupport', 'Extracurricular', 
                        'Sports', 'Music', 'Volunteering', 'GPA']

# Create a new DataFrame with the selected features
data_subset = data[features_of_interest]

# Correlation heatmap for selected features
correlation_matrix = data_subset.corr()
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Correlation Heatmap of Selected Features and GPA')      
plt.show()

# Boxplots for selected features
plt.figure(figsize=(12, 8))
for i, column in enumerate(features_of_interest[:-1]):  # Exclude GPA for boxplots
    plt.subplot(3, 3, i + 1)
    sns.boxplot(y=data[column])
    plt.title(f'Boxplot of {column}')
plt.tight_layout()
plt.show()

# Calculate and display the percentage of outliers for selected features
outlier_percentage = {}
for column in features_of_interest[:-1]:  # Exclude GPA for outlier calculation
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    outlier_percentage[column] = (len(outliers) / len(data)) * 100
    print(f"{column} - Outlier Percentage: {outlier_percentage[column]:.2f}%")

# Define features and target variable
X = data_subset.drop('GPA', axis=1)  # Features
y = data_subset['GPA']  # Target variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
rf_model = RandomForestRegressor(random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions with Random Forest
y_pred_rf = rf_model.predict(X_test)

# Evaluate Random Forest model
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)
print(f'Random Forest - Mean Squared Error: {mse_rf}')
print(f'Random Forest - R^2 Score: {r2_rf}')

# Train a Linear Regression model
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Make predictions with Linear Regression
y_pred_lr = lr_model.predict(X_test)

# Evaluate Linear Regression model
mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)
print(f'Linear Regression - Mean Squared Error: {mse_lr}')
print(f'Linear Regression - R^2 Score: {r2_lr}')

# For Logistic Regression, we need a binary target variable
if 'GPA' in data.columns:
    y_logistic = data['GPA']  # Replace with the actual binary target variable
    print("Unique values in the target variable for Logistic Regression:", y_logistic.unique())
    X_logistic = data.drop('GPA', axis=1)

    # Ensure the target variable is binary
    if y_logistic.nunique() == 2:  # Check if there are exactly two unique values
        # Split the data into training and testing sets for Logistic Regression
        X_train_logistic, X_test_logistic, y_train_logistic, y_test_logistic = train_test_split(X_logistic, y_logistic, test_size=0.2, random_state=42)

        # Train a Logistic Regression model
        logistic_model = LogisticRegression(max_iter=1000)
        logistic_model.fit(X_train_logistic, y_train_logistic)

        # Make predictions with Logistic Regression
        y_pred_logistic = logistic_model.predict(X_test_logistic)

        # Evaluate Logistic Regression model
        accuracy = accuracy_score(y_test_logistic, y_pred_logistic)
        cm = confusion_matrix(y_test_logistic, y_pred_logistic)
        print(f'Logistic Regression - Accuracy: {accuracy}')
        print(f'Confusion Matrix:\n{cm}')
    else:
        print("The target variable is not binary. Logistic Regression cannot be applied.")

# Visualize Actual vs Predicted for Random Forest
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_rf, label='Predicted', color='blue', alpha=0.6)
plt.scatter(y_test, y_test, label='Actual', color='orange', alpha=0.6)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', label='Perfect Prediction')
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs Predicted (Random Forest)')
plt.legend()
plt.show()


# Feature Importance
importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1]

# Visualize feature importance
plt.figure(figsize=(12, 6))
plt.title('Feature Importances (Random Forest)')
plt.bar(range(X.shape[1]), importances[indices], align='center')
plt.xticks(range(X.shape[1]), X.columns[indices], rotation=90)
plt.xlim([-1, X.shape[1]])
plt.show()
