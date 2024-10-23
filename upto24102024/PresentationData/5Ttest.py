from scipy.stats import ttest_ind

# T-test example
group1 = df[df['Industry_Type'] == 'Manufacturing']['Annual_Output']
group2 = df[df['Industry_Type'] == 'IT']['Annual_Output']
t_stat, p_value = ttest_ind(group1, group2)
print(f"T-Statistic: {t_stat}, P-Value: {p_value}")
