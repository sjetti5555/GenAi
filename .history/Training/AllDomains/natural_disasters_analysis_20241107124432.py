import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np

# Load the dataset
file_path = r'C:\Users\srira\OneDrive\Desktop\Gen_AI\Training\AllDomains\natural_disasters_2024.csv'  # Update this path
data = pd.read_csv(file_path)

# Display the first few rows of the dataset
print("First few rows of the dataset:")
print(data.head())

# Display basic information about the dataset
print(data.info())

# Display basic statistics
print("\nBasic statistics:")
print(data.describe())

# Check for missing values
print("\nMissing values in each column:")
print(data.isnull().sum())

# EDA: Visualizations
# 1. Count of disasters by type
plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='Disaster_Type', order=data['Disaster_Type'].value_counts().index)
plt.title('Count of Disasters by Type')
plt.xticks(rotation=45)
plt.show()

# 2. Distribution of Magnitude
plt.figure(figsize=(10, 6))
sns.histplot(data['Magnitude'], bins=30, kde=True)
plt.title('Distribution of Disaster Magnitudes')
plt.xlabel('Magnitude')
plt.ylabel('Frequency')
plt.show()

# 3. Total Economic Loss by Disaster Type
plt.figure(figsize=(10, 6))
sns.barplot(data=data, x='Disaster_Type', y='Economic_Loss($)', estimator=sum, errorbar=None)
plt.title('Total Economic Loss by Disaster Type')
plt.xticks(rotation=45)
plt.show()

# 4. Scatter plot of Fatalities vs. Economic Loss
plt.figure(figsize=(10, 6))
sns.scatterplot(data=data, x='Economic_Loss($)', y='Fatalities', hue='Disaster_Type', alpha=0.7)
plt.title('Fatalities vs. Economic Loss')
plt.xlabel('Economic Loss ($)')
plt.ylabel('Fatalities')
plt.legend()
plt.show()

# Prepare data for PCA
# Convert categorical variables to numeric using one-hot encoding
data_encoded = pd.get_dummies(data, columns=['Disaster_Type', 'Location'], drop_first=True)

# Separate features and target variable
X = data_encoded.drop(['Disaster_ID', 'Date', 'Fatalities', 'Economic_Loss($)'], axis=1)  # Features
y = data_encoded['Economic_Loss($)']  # Target variable

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA
pca = PCA(n_components=2)  # Reduce to 2 dimensions for visualization
X_pca = pca.fit_transform(X_scaled)

# Create a DataFrame for PCA results
pca_df = pd.DataFrame(data=X_pca, columns=['PC1', 'PC2'])
pca_df['Economic_Loss($)'] = y.values  # Add the target variable for visualization

# Visualize PCA results
plt.figure(figsize=(10, 6))
scatter = plt.scatter(data=pca_df, x='PC1', y='PC2', c=pca_df['Economic_Loss($)'], cmap='viridis', alpha=0.7)
plt.title('PCA of Natural Disasters Data')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar(scatter, label='Economic Loss ($)')
plt.grid()
plt.show()

# Train a Decision Tree model
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
model = DecisionTreeRegressor(random_state=42)
model.fit(X_train, y_train)

# Predictions and evaluation
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R-squared: {r2}') 