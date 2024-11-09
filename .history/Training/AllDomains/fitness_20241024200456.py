import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = rC:\Users\srira\OneDrive\Desktop\Gen_AI\Training\AllDomains\mturkfitbit_export_3.12.16-4.11.16\Fitabase Data 3.12.16-4.11.16\minuteSleep_merged.csv # Update this path
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

# Calculate the correlation matrix
correlation_matrix = numeric_data.corr()

# Visualize the correlation matrix
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()
