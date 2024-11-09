import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = r'C:\Users\srira\OneDrive\Desktop\Gen_AI\Training\AllDomains\Healthcare-Diabetes.csv' # Update this path
data = pd.read_csv(file_path)

# Display the first few rows of the dataset
print("First few rows of the dataset:")
print(data.head())

# Display basic statistics
print("\nBasic statistics:")
print(data.describe())

# Check for missing values
print("\nMissing values in each column:")
print(data.isnull().sum())

# Convert date columns to datetime if necessary
# Replace 'date_column_name' with the actual name of your date column
if 'date_column_name' in data.columns:
    data['date_column_name'] = pd.to_datetime(data['date_column_name'], errors='coerce')

# Drop non-numeric columns for correlation analysis
numeric_data = data.select_dtypes(include=['number'])

# Draw boxplots for outliers
plt.figure(figsize=(12, 6))
for i, column in enumerate(numeric_data.columns):  # Use numeric_data.columns here
    plt.subplot(2, (len(numeric_data.columns) + 1) // 2, i + 1)  # Create subplots
    sns.boxplot(y=numeric_data[column])  # Use numeric_data[column] for boxplot
    plt.title(f'Boxplot of {column}')
    plt.ylabel(column)

plt.tight_layout()
plt.show()

# Calculate the correlation matrix
correlation_matrix = numeric_data.corr()

# Visualize the correlation matrix
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()
