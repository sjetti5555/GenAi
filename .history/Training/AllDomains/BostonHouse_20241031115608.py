import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Load the dataset
file_path = r'C:\Users\srira\OneDrive\Desktop\Gen_AI\Training\AllDomains\boston.csv' # Update this path
data = pd.read_csv(file_path)