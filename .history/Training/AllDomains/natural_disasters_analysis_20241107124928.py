import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from mlxtend.frequent_patterns import apriori, association_rules
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
# 1. Boxplot for outlier detection
plt.figure(figsize=(10, 6))
sns.boxplot(data=data[['Magnitude', 'Fatalities', 'Economic_Loss($)']])
plt.title('Boxplot of Magnitude, Fatalities, and Economic Loss')
plt.ylabel('Values')
plt.grid()
plt.show()

# 2. Count of disasters by type
plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='Disaster_Type', order=data['Disaster_Type'].value_counts().index)
plt.title('Count of Disasters by Type')
plt.xticks(rotation=45)
plt.show()

# 3. Distribution of Magnitude
plt.figure(figsize=(10, 6))
sns.histplot(data['Magnitude'], bins=30, kde=True)
plt.title('Distribution of Disaster Magnitudes')
plt.xlabel('Magnitude')
plt.ylabel('Frequency')
plt.show()

# 4. Total Economic Loss by Disaster Type
plt.figure(figsize=(10, 6))
sns.barplot(data=data, x='Disaster_Type', y='Economic_Loss($)', estimator=sum, errorbar=None)
plt.title('Total Economic Loss by Disaster Type')
plt.xticks(rotation=45)
plt.show()

# 5. Scatter plot of Fatalities vs. Economic Loss
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

# Decision Tree
decision_tree_model = DecisionTreeRegressor(random_state=42)
decision_tree_model.fit(X_train, y_train)
y_pred_dt = decision_tree_model.predict(X_test)
mse_dt = mean_squared_error(y_test, y_pred_dt)
r2_dt = r2_score(y_test, y_pred_dt)
print(f'Decision Tree - Mean Squared Error: {mse_dt}, R-squared: {r2_dt}')

# Random Forest
random_forest_model = RandomForestRegressor(random_state=42)
random_forest_model.fit(X_train, y_train)
y_pred_rf = random_forest_model.predict(X_test)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)
print(f'Random Forest - Mean Squared Error: {mse_rf}, R-squared: {r2_rf}')

# Linear Regression
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
y_pred_lr = linear_model.predict(X_test)
mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)
print(f'Linear Regression - Mean Squared Error: {mse_lr}, R-squared: {r2_lr}')

# Logistic Regression (for demonstration, assuming we want to predict a binary outcome)
# Create a binary target variable for Logistic Regression
data['High_Economic_Loss'] = (data['Economic_Loss($)'] > data['Economic_Loss($)'].median()).astype(int)
y_logistic = data['High_Economic_Loss']
X_logistic = data_encoded.drop(['Disaster_ID', 'Date', 'High_Economic_Loss', 'Economic_Loss($)'], axis=1)

# Train-test split for Logistic Regression
X_train_log, X_test_log, y_train_log, y_test_log = train_test_split(X_logistic, y_logistic, test_size=0.2, random_state=42)

# Logistic Regression
logistic_model = LogisticRegression(max_iter=1000)
logistic_model.fit(X_train_log, y_train_log)
y_pred_log = logistic_model.predict(X_test_log)
accuracy_log = logistic_model.score(X_test_log, y_test_log)
print(f'Logistic Regression - Accuracy: {accuracy_log}')

# Association Rule Mining
# For association rules, we need to create a suitable DataFrame
# Here we will use the Disaster_Type and Location for association rules
association_data = data[['Disaster_Type', 'Location']]
association_data = association_data.groupby(['Disaster_Type', 'Location']).size().reset_index(name='Count')
association_data = association_data[association_data['Count'] > 1]  # Filter for meaningful associations

# One-hot encode for association rules
association_encoded = pd.get_dummies(association_data[['Disaster_Type', 'Location']])
frequent_itemsets = apriori(association_encoded, min_support=0.01, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)

print("\nAssociation Rules:")
print(rules)
