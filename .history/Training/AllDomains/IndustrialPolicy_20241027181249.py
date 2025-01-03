import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Set random seed for reproducibility
np.random.seed(42)

# Define parameters
years = list(range(2014, 2024))  # 10 years of data
regions = ["Visakhapatnam", "Vijayawada", "Guntur", "Kakinada", "Nellore"]
sectors = ["Manufacturing", "Technology", "Agriculture", "Healthcare", "Energy"]

# Generate 5000+ rows of synthetic data with irregularities
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

# Visualizing Historical Data for Each Sector
for sector in sectors:
    sector_data = df[df['Sector'] == sector]
    
    plt.figure(figsize=(14, 6))
    
    # Historical Investment Trend
    plt.subplot(1, 2, 1)
    sns.lineplot(data=sector_data, x="Year", y="Investment", label="Investment")
    plt.title(f"{sector} Sector - Historical Investment Trend")
    plt.xlabel("Year")
    plt.ylabel("Investment (INR crore)")
    
    # Historical Growth Rate Trend
    plt.subplot(1, 2, 2)
    sns.lineplot(data=sector_data, x="Year", y="Growth Rate (%)", color="orange", label="Growth Rate (%)")
    plt.title(f"{sector} Sector - Historical Growth Rate Trend")
    plt.xlabel("Year")
    plt.ylabel("Growth Rate (%)")
    
    plt.tight_layout()
    plt.show()

# Forecasting Future Trends with Linear Regression
future_years = np.array([2024, 2025, 2026, 2027, 2028]).reshape(-1, 1)
predictions = {}

for sector in sectors:
    sector_data = df[df['Sector'] == sector]
    X = sector_data[['Year']]
    y_investment = sector_data['Investment']
    y_growth_rate = sector_data['Growth Rate (%)']
    
    # Linear regression models for investment and growth rate
    model_investment = LinearRegression().fit(X, y_investment)
    model_growth = LinearRegression().fit(X, y_growth_rate)
    
    # Predictions
    investment_pred = model_investment.predict(future_years)
    growth_pred = model_growth.predict(future_years)
    
    predictions[sector] = {'Years': future_years.flatten(), 
                           'Investment': investment_pred, 
                           'Growth Rate': growth_pred}

# Visualizing Future Predictions for Each Sector
for sector in sectors:
    plt.figure(figsize=(14, 6))
    
    # Investment Forecast
    plt.subplot(1, 2, 1)
    plt.plot(predictions[sector]['Years'], predictions[sector]['Investment'], marker='o', label='Predicted Investment')
    plt.title(f"{sector} Sector - Investment Forecast")
    plt.xlabel("Year")
    plt.ylabel("Investment (INR crore)")
    plt.legend()
    
    # Growth Rate Forecast
    plt.subplot(1, 2, 2)
    plt.plot(predictions[sector]['Years'], predictions[sector]['Growth Rate'], marker='o', color='orange', label='Predicted Growth Rate')
    plt.title(f"{sector} Sector - Growth Rate Forecast")
    plt.xlabel("Year")
    plt.ylabel("Growth Rate (%)")
    plt.legend()
    
    plt.tight_layout()
    plt.show()
