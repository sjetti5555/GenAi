import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Define parameters
years = list(range(2014, 2024))  # 10 years of data
regions = ["Visakhapatnam", "Vijayawada", "Guntur", "Kakinada", "Nellore"]
sectors = ["Manufacturing", "Technology", "Agriculture", "Healthcare", "Energy"]

# Generate 5000+ rows of synthetic data
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

# Display the first few rows
df.head()
