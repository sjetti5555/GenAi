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
data = pd.read_csv(file_path)

# Display the first few rows of the dataset
print(data.head())
print(data.info())
print(data.describe())

# Separate features and target variable
X = data.drop('CRIM', axis=1)  # Drop the 'CRIM' column to use the rest as features
y = data['CRIM']  # 'CRIM' is the target variable

# Box plot for outliers in the target variable
plt.figure(figsize=(10, 6))
sns.boxplot(y=y)
plt.title('Boxplot of CRIM (Per Capita Crime Rate)')
plt.ylabel('CRIM')
plt.grid()
plt.show()

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Correlation heatmap
plt.figure(figsize=(12, 8))
correlation_matrix = data.corr()  # Calculate the correlation matrix
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .8})
plt.title('Correlation Heatmap of Boston Housing Data')
plt.show()

# Visualize CRIM against NOX (or any other feature)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=data, x='NOX', y='CRIM', hue='CRIM', palette='viridis', alpha=0.7)
plt.title('CRIM vs NOX (Nitric Oxides Concentration)')
plt.xlabel('NOX (Nitric Oxides Concentration)')
plt.ylabel('CRIM (Per Capita Crime Rate)')
plt.grid()
plt.show()

# Apply PCA
pca = PCA()
X_pca = pca.fit_transform(X_scaled)

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
X_pca_reduced = pca.fit_transform(X_scaled)

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