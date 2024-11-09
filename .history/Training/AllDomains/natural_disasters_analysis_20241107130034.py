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
from sklearn.cluster import KMeans
from mlxtend.frequent_patterns import apriori, association_rules
import geopandas as gpd
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

# Clustering disasters using KMeans
kmeans = KMeans(n_clusters=4, random_state=42)  # Adjust the number of clusters as needed
data['Cluster'] = kmeans.fit_predict(X_scaled)

# Visualize clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(data=data, x='Economic_Loss($)', y='Fatalities', hue='Cluster', palette='Set1', alpha=0.7)
plt.title('Clusters of Disasters')
plt.xlabel('Economic Loss ($)')
plt.ylabel('Fatalities')
plt.legend(title='Cluster')
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

# Debugging: Check if the column was created successfully
print("\nColumns in the original data after adding High_Economic_Loss:")
print(data.columns)

# Convert categorical variables to numeric using one-hot encoding
data_encoded = pd.get_dummies(data, columns=['Disaster_Type', 'Location'], drop_first=True)

# Debugging: Check columns in the encoded data
print("\nColumns in the encoded data:")
print(data_encoded.columns)

# Separate features and target variable
# Ensure 'High_Economic_Loss' is in the data_encoded DataFrame
if 'High_Economic_Loss' in data_encoded.columns:
    X_logistic = data_encoded.drop(['Disaster_ID', 'Date', 'High_Economic_Loss', 'Economic_Loss($)'], axis=1)
else:
    print("High_Economic_Loss column not found in data_encoded.")
    # Handle the case where the column is not found
    X_logistic = data_encoded.drop(['Disaster_ID', 'Date', 'Economic_Loss($)'], axis=1)  # Adjust as needed

y_logistic = data['High_Economic_Loss']  # Use the original data for the target variable

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

# Mapping disasters by country
# Create a GeoDataFrame for mapping
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Count disasters by country
disaster_counts = data['Location'].value_counts().reset_index()
disaster_counts.columns = ['Country', 'Count']

# Merge with world map
world = world.merge(disaster_counts, how="left", left_on="name", right_on="Country")

# Plotting the map
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
world.boundary.plot(ax=ax, linewidth=1)
world.plot(column='Count', ax=ax, legend=True,
           legend_kwds={'label': "Number of Disasters by Country",
                        'orientation': "horizontal"},
           missing_kwds={"color": "lightgrey"})
plt.title('Map of Disasters by Country')
plt.show()
