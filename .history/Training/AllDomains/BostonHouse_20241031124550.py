import pandas as pd                         
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import numpy as np

# Load the dataset
file_path = r'C:\Users\srira\OneDrive\Desktop\Gen_AI\Training\AllDomains\boston.csv'  # Update this path
data = pd.read_csv(file_path, header=None)

# Assign column names
data.columns = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']

# Display the first few rows of the dataset
print(data.head())
print(data.info())
print(data.describe())

# Check for non-numeric columns
print(data.dtypes)

# Convert non-numeric columns to numeric if necessary
# For this dataset, all columns should be numeric, so ensure they are treated as such
for column in data.columns:
    data[column] = pd.to_numeric(data[column], errors='coerce')  # Convert to numeric, coercing errors to NaN

# Drop any rows with NaN values (if any)
data.dropna(inplace=True)

# Separate features and target variable
X = data.drop('MEDV', axis=1)  # Features
y = data['MEDV']  # Target variable

# Check the data types of X to ensure they are all numeric
print(X.dtypes)

# Box plots for all numeric columns on a single page
numeric_columns = data.select_dtypes(include=[np.number]).columns  # Select numeric columns

plt.figure(figsize=(15, 10))
for i, column in enumerate(numeric_columns, 1):
    plt.subplot(4, 4, i)
    sns.boxplot(y=data[column])
    plt.title(f'Boxplot of {column}')
    plt.ylabel(column)
    plt.grid()

plt.tight_layout()
plt.show()

# Distribution plots for all numeric columns on a single page
plt.figure(figsize=(15, 10))
for i, column in enumerate(numeric_columns, 1):
    plt.subplot(4, 4, i)
    sns.histplot(data[column], kde=True, bins=30)  # KDE for density estimation
    plt.title(f'Distribution of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')

plt.tight_layout()
plt.show()

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train a Random Forest model
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions and evaluation
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

