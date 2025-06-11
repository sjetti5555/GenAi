import pandas as pd
import numpy as np

# Generate random dataset
data = {
    "Industry_Type": np.random.choice(['Manufacturing', 'IT', 'Agriculture'], 100),
    "Workforce_Size": np.random.randint(50, 1000, size=100),
    "Annual_Output": np.random.uniform(100000, 5000000, size=100)
}
df = pd.DataFrame(data)
df.to_csv('data/industry_data_presentation.csv', index=False)

# Calculate mean, median, mode
mean_workforce = df['Workforce_Size'].mean()
median_workforce = df['Workforce_Size'].median()
mode_industry = df['Industry_Type'].mode()[0]
print(f"Mean Workforce: {mean_workforce}, Median Workforce: {median_workforce}, Mode Industry: {mode_industry}")
