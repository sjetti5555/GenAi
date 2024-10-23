from scipy.stats import norm
import matplotlib.pyplot as plt

# Generate random data for normal distribution
data = norm.rvs(size=1000, loc=0, scale=1)
plt.hist(data, bins=30, density=True, alpha=0.6, color='g')

# Plot normal distribution curve
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x)
plt.plot(x, p, 'k', linewidth=2)
plt.title("Normal Distribution Curve")
plt.show()
