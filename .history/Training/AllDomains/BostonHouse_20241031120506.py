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
X = data.drop('TAX', axis=1)  # Drop the 'TAX' column to use the rest as features
y = data['TAX']  # 'TAX' is the target variable

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

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
# You can choose to keep a certain number of components, e.g., 2 or 3
pca = PCA(n_components=2)  # Change this to the desired number of components
X_pca_reduced = pca.fit_transform(X_scaled)

# Create a DataFrame for the PCA results
pca_df = pd.DataFrame(data=X_pca_reduced, columns=['PC1', 'PC2'])
pca_df['TAX'] = y.values  # Add the target variable for visualization

# Visualize the PCA results
plt.figure(figsize=(10, 6))
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='TAX', palette='viridis', alpha=0.7)
plt.title('PCA of Boston Housing Data')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend(title='TAX')
plt.grid()
plt.show()