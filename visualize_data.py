import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add the project root to the Python path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.config import PROJ_ROOT

def visualize_rpe_data(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Extract time and RPE values
    time = df['Time (s)']
    rpe = df['RPE Value']
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    
    # Plot the RPE data
    sns.scatterplot(x=time, y=rpe, color='blue', label='RPE Data')
    sns.lineplot(x=time, y=rpe, color='blue', alpha=0.5)
    
    # Plot the straight line from first to last datapoint
    plt.plot([time.iloc[0], time.iloc[-1]], [rpe.iloc[0], rpe.iloc[-1]], 
             color='red', linestyle='--', label='Straight Line')
    
    # Customize the plot
    plt.title('RPE Data Visualization', fontsize=16)
    plt.xlabel('Time (s)', fontsize=12)
    plt.ylabel('RPE Value', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle=':', alpha=0.7)
    
    # Show the plot
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # List all CSV files in the data directory
    data_dir = PROJ_ROOT 
    csv_files = list(data_dir.glob('*.csv'))
    
    if not csv_files:
        print("No CSV files found in the data directory.")
    else:
        print("Available CSV files:")
        for i, file in enumerate(csv_files):
            print(f"{i+1}. {file.name}")
        
        # Ask user to select a file
        while True:
            try:
                choice = int(input("Enter the number of the file you want to visualize: ")) - 1
                if 0 <= choice < len(csv_files):
                    selected_file = csv_files[choice]
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Visualize the selected file
        visualize_rpe_data(selected_file)