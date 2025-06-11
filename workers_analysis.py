import csv
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats # type: ignore

# Generate sample data
def generate_worker_data(num_workers, num_tasks):
    data = []
    for worker_id in range(1, num_workers + 1):
        for task_id in range(1, num_tasks + 1):
            # Generate task duration with some variation
            base_duration = random.uniform(1, 8)  # Base duration between 1 and 8 hours
            variation = random.uniform(0.8, 1.2)  # 20% variation
            duration = round(base_duration * variation, 2)
            data.append([worker_id, task_id, duration])
    return data

# Write data to CSV
def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Worker ID', 'Task ID', 'Task Duration (hours)'])
        writer.writerows(data)

# Read data from CSV
def read_from_csv(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            data.append([int(row[0]), int(row[1]), float(row[2])])
    return data

# Analyze worker performance
def analyze_performance(data):
    worker_performances = {}
    for row in data:
        worker_id, _, duration = row
        if worker_id not in worker_performances:
            worker_performances[worker_id] = []
        worker_performances[worker_id].append(duration)
    
    overall_durations = [duration for durations in worker_performances.values() for duration in durations]
    overall_mean = np.mean(overall_durations)
    overall_std = np.std(overall_durations)
    
    worker_stats = {}
    for worker_id, durations in worker_performances.items():
        mean = np.mean(durations)
        std = np.std(durations)
        z_score = (mean - overall_mean) / overall_std
        worker_stats[worker_id] = {
            'mean': mean,
            'std': std,
            'z_score': z_score
        }
    
    return worker_stats, overall_mean, overall_std

# Plot performance distribution
def plot_performance_distribution(data, worker_stats, overall_mean, overall_std):
    plt.figure(figsize=(12, 6))
    
    # Plot overall distribution
    overall_durations = [duration for row in data for duration in [row[2]]]
    plt.hist(overall_durations, bins=30, alpha=0.5, color='gray', label='Overall Distribution')
    
    # Plot normal distribution curve
    x = np.linspace(min(overall_durations), max(overall_durations), 100)
    plt.plot(x, stats.norm.pdf(x, overall_mean, overall_std) * len(overall_durations) * (max(overall_durations) - min(overall_durations)) / 30,
             'r-', lw=2, label='Normal Distribution')
    
    plt.axvline(overall_mean, color='red', linestyle='dashed', linewidth=2, label='Overall Mean')
    plt.axvline(overall_mean - 2*overall_std, color='orange', linestyle='dashed', linewidth=2, label='2 Std Dev Below Mean')
    plt.axvline(overall_mean + 2*overall_std, color='orange', linestyle='dashed', linewidth=2, label='2 Std Dev Above Mean')
    
    plt.xlabel('Task Duration (hours)')
    plt.ylabel('Frequency')
    plt.title('Worker Performance Distribution')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

# Generate and save sample data
num_workers = 20
num_tasks = 50
worker_data = generate_worker_data(num_workers, num_tasks)
csv_filename = 'data/worker_performance.csv'
write_to_csv(worker_data, csv_filename)
print(f"Worker performance data has been generated and saved to {csv_filename}")

# Analyze the data
data = read_from_csv(csv_filename)
worker_stats, overall_mean, overall_std = analyze_performance(data)

# Print analysis results
print(f"\nOverall Performance Statistics:")
print(f"Mean task duration: {overall_mean:.2f} hours")
print(f"Standard deviation: {overall_std:.2f} hours")

print("\nWorker Performance Summary:")
for worker_id, stats in worker_stats.items():
    print(f"Worker {worker_id}:")
    print(f"  Mean task duration: {stats['mean']:.2f} hours")
    print(f"  Standard deviation: {stats['std']:.2f} hours")
    print(f"  Z-score: {stats['z_score']:.2f}")
    if stats['z_score'] < -2:
        print("  Performance: Significantly faster than average")
    elif stats['z_score'] > 2:
        print("  Performance: Significantly slower than average")
    else:
        print("  Performance: Within normal range")
    print()

# Plot the performance distribution
plot_performance_distribution(data, worker_stats, overall_mean, overall_std)