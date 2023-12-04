import os

import matplotlib.pyplot as plt
import pandas as pd

from scripts.utility.path_utils import get_path_from_root

# Load the transportation dataset
transportation_path = get_path_from_root("data", "interim", "cleaned_transportation.csv")
transportation_df = pd.read_csv(transportation_path)

# Load the review dataset
review_df = pd.read_csv(get_path_from_root("data", "interim", "flattened_review.csv"))

output_path = get_path_from_root("results", "eda", "Phase 2", "trips_data_analysis")


def monthly_trips():
    # Convert 'Date' column to datetime and set as index
    transportation_df['Date'] = pd.to_datetime(transportation_df['Date'])
    transportation_df.set_index('Date', inplace=True)

    # Group by month (regardless of the year) and sum the number of trips
    monthly_trips_corrected = transportation_df.groupby(transportation_df.index.month)['Number of Trips'].sum()

    # Rename index to month names for clarity in the graph
    monthly_trips_corrected.index = monthly_trips_corrected.index.map({
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
    })

    # Plotting the corrected data
    plt.figure(figsize=(12, 6))
    monthly_trips_plot = monthly_trips_corrected.plot(kind='bar')
    plt.title('Total Number of Trips per Month (Aggregated Over the Years)')
    plt.xlabel('Month')
    plt.ylabel('Number of Trips')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Save the plot
    plot_path = os.path.join(output_path,
                             'monthly_trips_plot.png')
    plt.savefig(plot_path)

    # Save the data to a CSV file
    csv_path = os.path.join(output_path,
                            'monthly_trips_corrected.csv')
    monthly_trips_corrected.to_csv(csv_path)


def monthly_avg_rating():
    """
       This function loads the review dataset, calculates the average star rating by month,
       and plots the data.

       Args:
       review_csv_path (str): Path to the review dataset CSV file.

       Returns:
       str: Path to the saved plot.
       """
    # Convert 'Date' column to datetime and set as index
    review_df['Date'] = pd.to_datetime(review_df['Date'])
    review_df.set_index('Date', inplace=True)

    # Resample the data to calculate the average star rating by month across all years
    monthly_avg_rating = review_df['stars'].resample('M').mean()

    # Plotting the data
    plt.figure(figsize=(12, 6))
    monthly_avg_rating.plot()
    plt.title('Average Star Rating by Month')
    plt.xlabel('Month')
    plt.ylabel('Average Rating')
    plt.grid(True)

    # Save the plot
    plot_path = os.path.join(output_path, 'monthly_avg_rating_plot.png')
    plt.savefig(plot_path)

    # Save the csv
    monthly_avg_rating = pd.DataFrame(monthly_avg_rating)
    monthly_avg_rating.to_csv(os.path.join(output_path, 'monthly_avg_rating.csv'))


def quarterly_trips():
    """
    Function to plot and save the quarterly trips data.

    Args:
    transportation_csv_path (str): Path to the transportation dataset CSV file.
    output_csv_path (str): Path to save the aggregated quarterly trips data as a CSV file.
    output_plot_path (str): Path to save the plot as an image.

    Returns:
    None
    """
    # Load the transportation dataset
    transportation_df = pd.read_csv(transportation_path)
    transportation_df['Date'] = pd.to_datetime(transportation_df['Date'])
    transportation_df.set_index('Date', inplace=True)

    # Define quarters
    quarters = {
        'Winter': [12, 1, 2],
        'Spring': [3, 4, 5],
        'Summer': [6, 7, 8],
        'Fall': [9, 10, 11]
    }

    # Function to map each month to its corresponding quarter
    def map_to_quarter(month):
        for quarter, months in quarters.items():
            if month in months:
                return quarter
        return None

    # Map each row in the dataset to its corresponding quarter
    transportation_df['Quarter'] = transportation_df.index.month.map(map_to_quarter)

    # Group by quarter and sum the number of trips
    quarterly_trips = transportation_df.groupby('Quarter')['Number of Trips'].sum()
    quarterly_trips = quarterly_trips.reindex(['Winter', 'Spring', 'Summer', 'Fall'])

    # Save the data to a CSV file
    quarterly_trips.to_csv(output_path)

    # Plotting the data
    plt.figure(figsize=(8, 6))
    quarterly_trips.plot(kind='bar')
    plt.title('Total Number of Trips per Quarter')
    plt.xlabel('Quarter')
    plt.ylabel('Number of Trips')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Save the plot
    plt.savefig(output_path)


def quarterly_avg_rating():
    """
    Function to plot and save the quarterly average rating data.

    Args:
    review_csv_path (str): Path to the review dataset CSV file.
    output_csv_path (str): Path to save the aggregated quarterly average ratings as a CSV file.
    output_plot_path (str): Path to save the plot as an image.

    Returns:
    None
    """
    # Load the review dataset
    review_df['Date'] = pd.to_datetime(review_df['Date'])
    review_df.set_index('Date', inplace=True)

    # Define quarters
    quarters = {
        'Winter': [12, 1, 2],
        'Spring': [3, 4, 5],
        'Summer': [6, 7, 8],
        'Fall': [9, 10, 11]
    }

    # Function to map each month to its corresponding quarter
    def map_to_quarter(month):
        for quarter, months in quarters.items():
            if month in months:
                return quarter
        return None

    # Map each row in the review dataset to its corresponding quarter
    review_df['Quarter'] = review_df.index.month.map(map_to_quarter)
    quarterly_avg_rating = review_df.groupby('Quarter')['stars'].mean().reindex(['Winter', 'Spring', 'Summer', 'Fall'])

    # Save the data to a CSV file
    quarterly_avg_rating.to_csv(output_path)

    # Plotting the data
    plt.figure(figsize=(8, 6))
    quarterly_avg_rating.plot(kind='bar')
    plt.title('Average Star Rating by Quarter')
    plt.xlabel('Quarter')
    plt.ylabel('Average Rating')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Save the plot
    plt.savefig(output_path)


def main():
    monthly_trips()
    monthly_avg_rating()
    quarterly_trips()
    quarterly_avg_rating()
