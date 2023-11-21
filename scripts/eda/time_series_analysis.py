import pandas as pd
import matplotlib.pyplot as plt
from scripts.utility.data_loader import get_review_df, get_google_trends_data
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def prepare_time_series_data(review_data, trends_data):
    # Preparing Yelp Review data
    review_data["date"] = pd.to_datetime(review_data["date"])
    review_data.set_index("date", inplace=True)
    monthly_reviews = review_data.resample("M").agg({"stars": "mean", "review_id": "count"})

    # Preparing Google Trend Data
    # Assuming Google Trends data is already in the correct format
    monthly_trends = trends_data.resample("M").mean()

    # Combine Yelp data and Google Trend data
    combined_data = pd.merge(monthly_reviews, monthly_trends, left_index=True, right_index=True, how="outer")
    return combined_data


def plot_combined_time_series(combined_data, title='Monthly Trends for Italian Restaurants',
                              file_name='monthly_trends.png'):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plotting Yelp Review Trends
    color = 'tab:blue'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Average Rating', color=color)
    ax1.plot(combined_data.index, combined_data['stars'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Plotting Google Trends Data
    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.set_ylabel('Google Search Interest', color=color)
    ax2.plot(combined_data.index, combined_data['Italian_Restaurant_in_PA'], color=color)  # Update column name
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(title)
    fig.tight_layout()
    plt.savefig(file_name)
    plt.show()


def main():
    review_data = get_review_df()
    google_trends_data = get_google_trends_data()

    if not review_data.empty and not google_trends_data.empty:
        combined_data = prepare_time_series_data(review_data, google_trends_data)
        plot_combined_time_series(combined_data, "Yelp Reviews and Google Trends Over Time", "combined_trends.png")
        logger.info("Combined time-series analysis completed and plot saved.")
    else:
        logger.error("Failed to load data for combined time-series analysis.")


if __name__ == "__main__":
    main()
