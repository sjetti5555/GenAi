import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress, norm, ttest_ind, chi2_contingency
import sqlite3
import random
import folium

# Step 1: Data Collection and Storage
# Simulate industry data for Andhra Pradesh
np.random.seed(42)
industry_data = {
    'industry_id': range(1, 101),
    'industry_type': np.random.choice(['Manufacturing', 'IT Services', 'Agriculture', 'Mining', 'Textiles'], 100),
    'location': np.random.choice(['Vijayawada', 'Visakhapatnam', 'Tirupati', 'Guntur', 'Kurnool'], 100),
    'workforce_size': np.random.randint(50, 1000, size=100),
    'annual_output_million': np.random.randint(10, 500, size=100)
}

industry_df = pd.DataFrame(industry_data)

# Store data into an SQLite database
conn = sqlite3.connect('andhra_pradesh_industry_data.db')
industry_df.to_sql('industry', conn, if_exists='replace', index=False)
print("Data stored in SQLite database.")

# Step 2: Descriptive Analysis
# Summary statistics
print("\nSummary Statistics:")
print(industry_df.describe())

# Distribution of industries by type
sns.countplot(data=industry_df, x='industry_type')
plt.title('Distribution of Industries by Type')
plt.xticks(rotation=45)
plt.show()

# Step 3: Modeling and Predictive Analysis
# Simulate a simple linear regression to predict annual output based on workforce size
slope, intercept, r_value, p_value, std_err = linregress(industry_df['workforce_size'], industry_df['annual_output_million'])
print(f"\nLinear Regression: Output = {slope:.2f} * Workforce Size + {intercept:.2f}")
print(f"R-squared: {r_value**2:.2f}")

# Step 4: Optimization and Decision Making
# Example: Allocation of resources based on workforce size (using a matrix)
resource_matrix = np.random.randint(100, 1000, (5, 5))  # Simulated subsidy allocation matrix
print("\nResource Allocation Matrix (Subsidies):")
print(resource_matrix)

# Step 5: Simulation and Risk Analysis
# Simulate market fluctuation using normal distribution
market_fluctuation = norm.rvs(loc=0, scale=1, size=1000)
plt.hist(market_fluctuation, bins=30, alpha=0.7, color='blue')
plt.title('Simulated Market Fluctuation')
plt.show()

# Step 6: Policy Implementation and Monitoring
# Example: Clustering analysis (K-Means can be used for more complexity)
industry_clusters = industry_df.groupby('location')['annual_output_million'].mean().sort_values()
print("\nIndustry Clusters Based on Average Output:")
print(industry_clusters)

# Step 7: Visualization and Reporting
# Create a basic map with Folium for industry locations
map_center = [15.9129, 79.7400]  # Approximate center of Andhra Pradesh
ap_map = folium.Map(location=map_center, zoom_start=6)

for index, row in industry_df.iterrows():
    folium.Marker(
        location=[random.uniform(15, 18), random.uniform(78, 82)],  # Random latitude and longitude
        popup=f"{row['industry_type']} - {row['location']}",
        tooltip=row['industry_type']
    ).add_to(ap_map)

# Save the map as an HTML file
ap_map.save("andhra_pradesh_industries_map.html")
print("Map saved as 'andhra_pradesh_industries_map.html'")

# Step 8: Testing the Data
# Example: T-test comparing two industry types' outputs
manufacturing_output = industry_df[industry_df['industry_type'] == 'Manufacturing']['annual_output_million']
it_output = industry_df[industry_df['industry_type'] == 'IT Services']['annual_output_million']
t_stat, p_value = ttest_ind(manufacturing_output, it_output)
print(f"\nT-test between Manufacturing and IT Services Outputs: t_stat = {t_stat:.2f}, p_value = {p_value:.4f}")

# Chi-square test for independence between industry type and location
contingency_table = pd.crosstab(industry_df['industry_type'], industry_df['location'])
chi2, p_val, dof, expected = chi2_contingency(contingency_table)
print(f"\nChi-square Test for Independence: chi2 = {chi2:.2f}, p_value = {p_val:.4f}")
