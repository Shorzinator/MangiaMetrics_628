import logging
import os

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

from scripts.utility.path_utils import get_path_from_root

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_business():
    path = "/Users/shouryamaheshwari/Desktop/UW/STAT 628/MangiaMetrics_628/data/interim/flattened_gis.csv"  # Update this to your CSV path
    try:
        df = pd.read_csv(path)
        # Assuming your CSV has columns named 'longitude' and 'latitude'
        # Convert to a GeoDataFrame
        gdf = gpd.GeoDataFrame(
            df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
        return gdf
    except Exception as e:
        logger.error(f"Error loading business data: {e}")
        return gpd.GeoDataFrame()


def load_geodata():
    path = \
        "/Users/shouryamaheshwari/Desktop/UW/STAT 628/MangiaMetrics_628/data/raw/shape_files_for_pa/pennsylvania_administrative.shp"  # Update with the correct path, excluding the file extension
    try:
        # Load the shapefile
        gdf = gpd.read_file(path)
        return gdf
    except Exception as e:
        logger.error(f"Error loading PA administrative shapefile: {e}")
        return gpd.GeoDataFrame()


def plot_restaurant_distribution(business_data, geo_data, title, file_name):
    # Set the figure size and create a plot axis
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plotting the PA map with distinct color and edge color
    if not geo_data.empty and 'geometry' in geo_data.columns:
        geo_data.plot(ax=ax, color="lightgrey", edgecolor="black")
    else:
        logger.error("No polygon data to plot for the base map.")

    # Ensuring the business data plots on top
    ax.set_zorder(1)  # Set zorder to put the business plot on top of the base map

    # Plotting Italian Restaurants on top of the base map
    business_data.plot(ax=ax, x='longitude', y='latitude', kind='scatter', color='red', label='Italian Restaurants',
                       alpha=0.5)

    # Set the title and labels
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()

    # Save the plot to a file
    plt.savefig(os.path.join(get_path_from_root("results", "eda", "Phase 1"), file_name), dpi=300)
    # plt.show()
    plt.close()


def main():
    business_data = load_business()
    geo_data = load_geodata()

    if not business_data.empty and not geo_data.empty:
        plot_restaurant_distribution(business_data, geo_data, "Distribution of Italian Restaurants in PA",
                                     "italian_restaurants_distribution_pa.png")
    else:
        logger.error("Failed to load data for visualization.")


if __name__ == "__main__":
    main()
