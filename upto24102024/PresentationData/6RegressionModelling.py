from sklearn.linear_model import LinearRegression
import numpy as np

# Linear Regression example
X = df[['Workforce_Size']].values
y = df['Annual_Output'].values
model = LinearRegression()
model.fit(X, y)

# Predict and plot regression line
y_pred = model.predict(X)
plt.scatter(X, y, color='blue')
plt.plot(X, y_pred, color='red')
plt.title('Regression Model: Workforce Size vs Annual Output')
plt.xlabel('Workforce Size')
plt.ylabel('Annual Output')
plt.show()
