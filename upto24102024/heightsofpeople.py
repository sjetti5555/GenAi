import numpy as np
import matplotlib.pyplot as plt

def input_heights():
    heights = []
    while True:
        height = input("Enter height in cm (or 'done' to finish): ")
        if height.lower() == 'done':
            break
        heights.append(float(height))
    return heights

def plot_height_distribution(heights):
    mean = np.mean(heights)
    std_dev = np.std(heights)

    x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 100)
    y = np.exp(-0.5 * ((x - mean) / std_dev)**2) / (std_dev * np.sqrt(2 * np.pi))

    plt.figure(figsize=(10, 6))
    plt.hist(heights, bins=10, density=True, alpha=0.7, color='skyblue')
    plt.plot(x, y, 'r-', lw=2)
    plt.title(f'Height Distribution (Mean: {mean:.2f}, Std Dev: {std_dev:.2f})')
    plt.xlabel('Height (cm)')
    plt.ylabel('Probability Density')
    plt.grid(True, alpha=0.3)
    plt.show()

# Main program
heights = input_heights()
if heights:
    plot_height_distribution(heights)
else:
    print("No heights entered. Exiting.")
