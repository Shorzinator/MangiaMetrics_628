import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point
from scripts.utility.path_utils import get_path_from_root
from scripts.utility.data_loader import get_clean_business_df, get_geodata
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def plot_restaurant_distribution(business_data, geo_data, title, file_name):
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plotting the PA map
    pa_map = geo_data.plot(ax=ax, color="lightgrey", edgecolor="black")

    # Plotting Italian Restaurants
    business_data.plot(ax=pa_map, x='longitude', y='latitude', kind='scatter',
                       color='red', label='Italian Restaurants', alpha=0.5)

    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.savefig(file_name)
    plt.close()


def main():
    business_data = get_clean_business_df()
    geo_data = get_geodata()

    if not business_data.empty and not geo_data.empty:
        plot_restaurant_distribution(business_data, geo_data, "Distribution of Italian Restaurants in PA",
                                     "italian_restaurants_distribution_pa.png")
    else:
        logger.error("Failed to load data for visualization.")


if __name__ == "__main__":
    main()
