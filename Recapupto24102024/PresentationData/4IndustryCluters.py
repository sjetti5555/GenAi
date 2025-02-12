from sklearn.cluster import KMeans
import seaborn as sns

# K-means clustering for industry data
kmeans = KMeans(n_clusters=3)
df['Cluster'] = kmeans.fit_predict(df[['Workforce_Size', 'Annual_Output']])

# Visualization
sns.scatterplot(data=df, x='Workforce_Size', y='Annual_Output', hue='Cluster')
plt.title('Industry Clusters')
plt.show()
