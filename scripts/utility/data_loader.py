import logging

import geopandas as gpd
import pandas as pd

from scripts.utility.path_utils import get_path_from_root

# Constants
CHUNK_SIZE = 10000  # Adjust based on system's memory capability

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Function to load data in chunks
def load_data_in_chunks(file_path, chunk_size):
    try:
        temp_df = pd.DataFrame()
        for chunk in pd.read_json(file_path, lines=True, chunksize=chunk_size):
            temp_df = pd.concat([temp_df, chunk])
        return temp_df
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {e}")
        return pd.DataFrame()


# Function to load business data
def get_business_df():
    business_path = get_path_from_root("data", "raw", "Yelp Data", "business.json")
    return load_data_in_chunks(business_path, CHUNK_SIZE)


# Function to load review data
def get_review_df():
    review_path = get_path_from_root("data", "raw", "Yelp Data", "review.json")
    return load_data_in_chunks(review_path, CHUNK_SIZE)


# Function to load cleaned business data
def get_clean_business_df():
    path = get_path_from_root("data", "interim", "cleaned_business.json")
    try:
        return pd.read_json(path, lines=True)
    except Exception as e:
        logger.error(f"Error loading cleaned business data: {e}")
        return pd.DataFrame()


# Function to load GeoJSON data
def get_geodata():
    path = get_path_from_root("data", "GIS Data", "export.geojson")
    try:
        return gpd.read_file(path)
    except Exception as e:
        logger.error(f"Error loading GeoJSON data: {e}")
        return gpd.GeoDataFrame()


def get_google_trends_data():
    path = get_path_from_root("data", "Google Trend Data", "InterestOverTime.csv")
    try:
        trends_data = pd.read_csv(path)
        trends_data['date'] = pd.to_datetime(trends_data['date'])  # Assuming there is a 'date' column
        trends_data.set_index('date', inplace=True)
        return trends_data
    except Exception as e:
        logger.error(f"Error in loading Google Trends data: {e}")
        return pd.DataFrame()
