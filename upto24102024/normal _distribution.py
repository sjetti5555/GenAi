import math

def normal_distribution(x, mean, std_dev):
    """
    Calculate the probability density function of the normal distribution.
    
    Parameters:
    x (float): The value for which to calculate the probability density
    mean (float): The mean (μ) of the distribution
    std_dev (float): The standard deviation (σ) of the distribution
    
    Returns:
    float: The probability density at x
    """
    coefficient = 1 / (std_dev * math.sqrt(2 * math.pi))
    exponent = -((x - mean) ** 2) / (2 * (std_dev ** 2))
    return coefficient * math.exp(exponent)

# Example usage
mean = 0
std_dev = 1
x = 1.5

pdf_value = normal_distribution(x, mean, std_dev)
print(f"PDF value for x={x}, mean={mean}, std_dev={std_dev}: {pdf_value:.6f}")

# To visualize the distribution, you can plot it using matplotlib
import numpy as np
import matplotlib.pyplot as plt

x_values = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 100)
y_values = [normal_distribution(x, mean, std_dev) for x in x_values]

plt.plot(x_values, y_values)
plt.title('Normal Distribution')
plt.xlabel('x')
plt.ylabel('Probability Density')
plt.grid(True)
plt.show()