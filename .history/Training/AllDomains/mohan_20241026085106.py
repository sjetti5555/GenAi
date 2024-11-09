# Calculate the correlation matrix, selecting only numeric columns
correlation_matrix = df.select_dtypes(include=[np.number]).corr()

# Create a heatmap with 'Purchased' as the dependent variable
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix[['total_amount']], annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation with total_amount')
plt.show()