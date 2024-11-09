import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.decomposition import PCA
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
# If 'ZN' is a categorical variable, you might want to drop it or convert it
# For this dataset, 'ZN' should be numeric, so ensure it is treated as such
data['ZN'] = pd.to_numeric(data['ZN'], errors='coerce')  # Convert to numeric, coercing errors to NaN

# Drop any rows with NaN values (if any)
data.dropna(inplace=True)

# Separate features and target variable
X = data.drop('CRIM', axis=1)  # Features
y = data['CRIM']  # Target variable

# Box plots for outliers in all numeric columns
numeric_columns = data.select_dtypes(include=[np.number]).columns  # Select numeric columns

# Create box plots for each numeric column
for column in numeric_columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(y=data[column])
    plt.title(f'Boxplot of {column}')
    plt.ylabel(column)
    plt.grid()
    plt.show()

# Standardize the features
scaler = StandardScaler()

# Correlation heatmap
plt.figure(figsize=(12, 8))
correlation_matrix = data.corr()  # Calculate the correlation matrix
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .8})
plt.title('Correlation Heatmap of Boston Housing Data')
plt.show()

# Apply PCA
pca = PCA()
X_pca = pca.fit_transform(X)

# Explained variance ratio
explained_variance = pca.explained_variance_ratio_

# Plot the explained variance
plt.figure(figsize=(10, 6))
plt.plot(range(1, len(explained_variance) + 1), explained_variance, marker='o', linestyle='--')
plt.title('Explained Variance by Principal Components')
plt.xlabel('Principal Component')
plt.ylabel('Variance Explained')
plt.xticks(range(1, len(explained_variance) + 1))
plt.grid()
plt.show()

# Optional: Transform the data to the PCA space
pca = PCA(n_components=2)  # Change this to the desired number of components
X_pca_reduced = pca.fit_transform(X)

# Create a DataFrame for the PCA results
pca_df = pd.DataFrame(data=X_pca_reduced, columns=['PC1', 'PC2'])
pca_df['CRIM'] = y.values  # Add the target variable for visualization

# Visualize the PCA results
plt.figure(figsize=(10, 6))
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='CRIM', palette='viridis', alpha=0.7)
plt.title('PCA of Boston Housing Data')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend(title='CRIM')
plt.grid()
plt.show()

# Train a Random Forest model
X_train, X_test, y_train, y_test = train_test_split(X_pca_reduced, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions and evaluation
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}')

# Box plots for outliers in all numeric columns
numeric_columns = data.select_dtypes(include=[np.number]).columns  # Select numeric columns

# Create box plots for each numeric column
for column in numeric_columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(y=data[column])
    plt.title(f'Boxplot of {column}')
    plt.ylabel(column)
    plt.grid()
    plt.show()