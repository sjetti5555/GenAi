import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Load the dataset
file_path = r'C:\Users\srira\OneDrive\Desktop\Gen_AI\Training\AllDomains\natural_disasters_2024.csv' # Update this path
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


# Preprocess the data
data['Quality'] = data['Quality'].map({'good': 1, 'bad': 0})  # Convert Quality to binary
features = ['Weight', 'Sweetness', 'Crunchiness', 'Juiciness', 'Ripeness', 'Acidity']
X = data[features]
y = data['Quality']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Mean Squared Error: {mse}')
print(f'R² Score: {r2}')

# Visualize the results
# 1. Perplexity plot (using Mean Squared Error as a proxy for perplexity)
plt.figure(figsize=(10, 5))
plt.plot(y_test.reset_index(drop=True), label='Actual Quality', marker='o')
plt.plot(y_pred, label='Predicted Quality', marker='x')
plt.title('Actual vs Predicted Quality')
plt.xlabel('Sample Index')
plt.ylabel('Quality (0 = bad, 1 = good)')
plt.legend()
plt.show()

# 2. Pie chart for quality distribution
quality_counts = data['Quality'].value_counts()
plt.figure(figsize=(8, 6))
plt.pie(quality_counts, labels=['Bad', 'Good'], autopct='%1.1f%%', startangle=90)
plt.title('Quality Distribution')
plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
plt.show()

# 3. Boxplots for all features grouped by Quality
plt.figure(figsize=(12, 8))
for i, column in enumerate(features):
    plt.subplot(2, 3, i + 1)  # Adjust the layout for 6 features
    sns.boxplot(x='Quality', y=column, data=data)
    plt.title(f'Boxplot of {column} by Quality')
    plt.xlabel('Quality (0 = bad, 1 = good)')
    plt.ylabel(column)
plt.tight_layout()
plt.show()



