import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Print the first few rows of the DataFrame
print("First few rows of the DataFrame:")
print(df.head(10))

# 1. Bar plot of total EV sales by state
plt.figure(figsize=(12, 6))
df.groupby('State')['EV_Sales_Quantity'].sum().sort_values(ascending=False).plot(kind='bar')
plt.title('Total EV Sales by State')
plt.xlabel('State')
plt.ylabel('Total EV Sales')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# 2. Pie chart of EV sales by vehicle type
plt.figure(figsize=(10, 10))
df.groupby('Vehicle_Type')['EV_Sales_Quantity'].sum().plot(kind='pie', autopct='%1.1f%%')
plt.title('EV Sales Distribution by Vehicle Type')
plt.ylabel('')
plt.show()

# 3. Line plot of EV sales trend over time
df['Date'] = pd.to_datetime(df['Date'])
monthly_sales = df.groupby('Date')['EV_Sales_Quantity'].sum().reset_index()
plt.figure(figsize=(12, 6))
plt.plot(monthly_sales['Date'], monthly_sales['EV_Sales_Quantity'])
plt.title('EV Sales Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Total EV Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. Bar plot of EV sales by vehicle category
plt.figure(figsize=(10, 6))
df.groupby('Vehicle_Category')['EV_Sales_Quantity'].sum().sort_values(ascending=False).plot(kind='bar')
plt.title('EV Sales by Vehicle Category')
plt.xlabel('Vehicle Category')
plt.ylabel('Total EV Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Additional analysis: Top 3 states by EV sales
top_3_states = df.groupby('State')['EV_Sales_Quantity'].sum().sort_values(ascending=False).head(3)
print("\nTop 3 states by EV sales:")
print(top_3_states)
