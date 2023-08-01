import datetime
import os

# Create timestamp for current run
timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

# Define paths for saving results
results_directory = f"./results/{timestamp}/runs"
plots_directory = f'./results/{timestamp}/plots'

# Create directories if they do not exist
os.makedirs(results_directory, exist_ok=True)
os.makedirs(plots_directory, exist_ok=True)
