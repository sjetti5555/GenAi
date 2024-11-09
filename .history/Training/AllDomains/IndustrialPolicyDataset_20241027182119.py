import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Define parameters
years = list(range(2014, 2024))  # 10 years of data
regions = ["Visakhapatnam", "Vijayawada", "Guntur", "Kakinada", "Nellore"]
sectors = ["Manufacturing", "Technology", "Agriculture", "Healthcare", "Energy"]

# Generate synthetic data with irregularities
data = []
for year in years:
    for region in regions:
        for sector in sectors:
            employment = np.random.randint(1000, 50000)
            investment = np.random.randint(50, 1000)
            growth_rate = np.random.uniform(-5, 20) if sector != "Agriculture" else np.random.uniform(-10, 15)
            exports = np.random.randint(10, 500)
            environmental_impact = np.random.choice(["Low", "Medium", "High"])
            revenue = investment * growth_rate / 100 + np.random.randint(100, 1000)
            policy_recommendation = "Increase Investment" if growth_rate > 10 else "Job Creation Program"
            
            # Introduce irregularities
            if np.random.rand() > 0.95:
                employment = np.nan  # Missing value
            if np.random.rand() > 0.95:
                investment = np.nan  # Missing value
            if np.random.rand() > 0.98:
                growth_rate *= 4  # Extreme outlier
            
            data.append([region, sector, year, employment, investment, growth_rate, exports, 
                         environmental_impact, revenue, policy_recommendation])

# Convert to DataFrame and add duplicates
df = pd.DataFrame(data, columns=["Region", "Sector", "Year", "Employment", "Investment", 
                                 "Growth Rate (%)", "Exports", "Environmental Impact", 
                                 "Revenue", "Policy Recommendation"])

# Introduce duplicates
df = pd.concat([df, df.sample(10)], ignore_index=True)

# Data Cleaning: Remove duplicates and handle missing values
df.drop_duplicates(inplace=True)
df['Employment'].fillna(df['Employment'].median(), inplace=True)
df['Investment'].fillna(df['Investment'].median(), inplace=True)

# Outlier Detection and Capping
upper_limit = df['Growth Rate (%)'].quantile(0.95)
lower_limit = df['Growth Rate (%)'].quantile(0.05)
df['Growth Rate (%)'] = np.where(df['Growth Rate (%)'] > upper_limit, upper_limit,
                                 np.where(df['Growth Rate (%)'] < lower_limit, lower_limit, df['Growth Rate (%)']))

# Describe the cleaned dataset
description = df.describe(include='all')
info = df.info()

# Save cleaned dataset to CSV
output_path = '/mnt/data/andhra_pradesh_industrial_policy_data_cleaned.csv'
df.to_csv(output_path, index=False)

output_path, description
