import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scripts.utility.data_loader import get_clean_business_df


def aggregate_and_visualize(df):
    """
    Aggregate the data by county and date and visualize the results.
    """
    # Aggregate the data by county and month
    monthly_data = df.resample('M').sum()

    # Generate a bar plot for the total number of trips per month
    monthly_data['Number of Trips'].plot(kind='bar', figsize=(12, 7))
    plt.title('Total Number of Trips per Month in PA')
    plt.xlabel('Month')
    plt.ylabel('Number of Trips')
    plt.show()

    # Generate a line plot for the average number of trips per category
    trip_categories = ['Number of Trips <1', 'Number of Trips 1-3', 'Number of Trips 3-5',
                       'Number of Trips 5-10', 'Number of Trips 10-25', 'Number of Trips 25-50',
                       'Number of Trips 50-100', 'Number of Trips 100-250', 'Number of Trips 250-500']
    avg_trips = df[trip_categories].mean()
    avg_trips.plot(kind='line', figsize=(12, 7))
    plt.title('Average Number of Trips by Distance Category in PA')
    plt.xlabel('Distance Category')
    plt.ylabel('Average Number of Trips')
    plt.xticks(rotation=45)
    plt.show()

    # Visualizing the distribution of 'Number of Trips >=500'
    df['Number of Trips >=500'].plot(kind='hist', bins=50, figsize=(12, 7))
    plt.title('Distribution of Number of Trips >=500 in PA')
    plt.xlabel('Number of Trips >=500')
    plt.ylabel('Frequency')
    plt.show()


def main():
    df = pd.read_csv(
        "/Users/shouryamaheshwari/Desktop/UW/STAT 628/MangiaMetrics_628/data/interim/cleaned_transportation.csv")
    aggregate_and_visualize(df)
