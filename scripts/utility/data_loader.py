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
    path = get_path_from_root("data", "interim", "flattened_business.csv")
    try:
        # Attempt to read the file in the JSON lines format
        return pd.read_csv(path)
    except ValueError as e:
        logger.error(f"Error loading cleaned business data: {e}")
        try:
            # Attempt to read a JSON file that is an array of objects
            return pd.read_csv(path)
        except ValueError as e2:
            logger.error(f"Error loading cleaned business data: {e2}")
    return pd.DataFrame()


def get_clean_review_df():
    path = get_path_from_root("data", "interim", "flattened_review.csv")
    try:
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"Error loading cleaned review data: {e}")
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
    path = get_path_from_root("data", "raw", "Google Trend Data", "InterestOverTime_since2004.csv")
    try:
        trends_data = pd.read_csv(path)
        trends_data['Month'] = pd.to_datetime(trends_data['Month'])
        trends_data.set_index('Month', inplace=True)
        return trends_data
    except Exception as e:
        logger.error(f"Error in loading Google Trends data: {e}")
        return pd.DataFrame()


def get_clean_transportation_df():
    path = get_path_from_root("data", "interim", "cleaned_transportation.csv")
    try:
        transportation_df = pd.read_csv(path)
        transportation_df['Date'] = pd.to_datetime(transportation_df['Date'])
        return transportation_df

    except Exception as e:
        logger.error(f"Error in loading Transportation data: {e}")
        return pd.DataFrame()
