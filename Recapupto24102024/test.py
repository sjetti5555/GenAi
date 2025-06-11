
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_json('data/t20_wc_player_info.json')

print(df[df['team']=='India'])

plt.l(df['name'],df['team'])
plt.show()



# Different graph formats available in matplotlib:
# 1. Line plot: plt.plot(df['Age'])
# 2. Scatter plot: plt.scatter(df.index, df['Age'])
# 3. Bar plot: plt.bar(df.index, df['Age'])
# 4. Histogram: plt.hist(df['Age'])
# 5. Box plot: plt.boxplot(df['Age'])
# 6. Violin plot: plt.violinplot(df['Age'])
# 7. Pie chart: plt.pie(df['Age'].value_counts())
# 8. Area plot: plt.fill_between(df.index, df['Age'])
# 9. Heatmap: plt.imshow(df.corr())
# 10. Contour plot: plt.contour(df['Age'].values.reshape(10,10))

# Different file formats for data storage and exchange:

# 1. CSV (Comma-Separated Values)
df.to_csv('data/data.csv', index=False)
# Reading: pd.read_csv('data/data.csv')

# 2. JSON (JavaScript Object Notation)
df.to_json('data/data.json', orient='records')
# Reading: pd.read_json('data/data.json')

# 3. Excel
df.to_excel('data.xlsx', index=False)
# Reading: pd.read_excel('data.xlsx')

# 4. Parquet (columnar storage)
df.to_parquet('data.parquet')
# Reading: pd.read_parquet('data.parquet')

# 5. HDF5 (Hierarchical Data Format)
df.to_hdf('data.h5', key='df', mode='w')
# Reading: pd.read_hdf('data.h5', 'df')

# 6. Feather (fast, language-agnostic binary format)
df.to_feather('data.feather')
# Reading: pd.read_feather('data.feather')

# 7. Pickle (Python-specific serialization)
df.to_pickle('data.pkl')
# Reading: pd.read_pickle('data.pkl')

# Note: Some formats may require additional libraries to be installed

