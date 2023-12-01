import os

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator

# Assuming the 'path_utils.py' script has a function 'get_path_from_root' that constructs the path correctly.
from scripts.utility.path_utils import get_path_from_root


def aggregate_and_visualize(df, path_to_save):
    """
    Aggregate the data by county and date and visualize the results.
    """
    # Ensure the directory exists
    os.makedirs(path_to_save, exist_ok=True)

    # Aggregate the data by county and month
    monthly_data = df.resample('M').sum()

    # Generate a bar plot for the total number of trips per month
    fig, ax = plt.subplots(figsize=(15, 7))
    monthly_data['Number of Trips'].plot(kind='bar', ax=ax)
    ax.set_title('Total Number of Trips per Month in PA', fontsize=16)
    ax.set_xlabel('Month', fontsize=14)
    ax.set_ylabel('Number of Trips', fontsize=14)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(path_to_save, "Total_trips_pm.png"))
    plt.show()

    # Generate a line plot for the average number of trips per category
    trip_categories = ['Number of Trips <1', 'Number of Trips 1-3', 'Number of Trips 3-5',
                       'Number of Trips 5-10', 'Number of Trips 10-25', 'Number of Trips 25-50',
                       'Number of Trips 50-100', 'Number of Trips 100-250', 'Number of Trips 250-500']
    avg_trips = df[trip_categories].mean(axis=0)
    fig, ax = plt.subplots(figsize=(15, 7))
    avg_trips.plot(kind='line', marker='o', ax=ax)
    ax.set_title('Average Number of Trips by Distance Category in PA', fontsize=16)
    ax.set_xlabel('Distance Category', fontsize=14)
    ax.set_ylabel('Average Number of Trips', fontsize=14)
    plt.xticks(range(len(trip_categories)), trip_categories, rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(path_to_save, "Avg_trips_by_distance_cat.png"))
    plt.show()


def main():
    try:
        # Adjust the path as necessary.
        file_path = get_path_from_root("data", "interim", "cleaned_transportation.csv")
        df = pd.read_csv(file_path)

        # Convert 'Date' to datetime and set as index
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)

        # Directory to save plots
        path_to_save = get_path_from_root("results", "eda")

        aggregate_and_visualize(df, path_to_save)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
