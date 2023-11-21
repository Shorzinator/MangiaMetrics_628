import pandas as pd
import logging
import geopandas as gpd
from scripts.eda.eda_initial import load_data_in_chunks
from scripts.utility.path_utils import get_path_from_root

chunk_size = 10000  # Adjust based on system's memory capability

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_business_df():
    # Define paths to data
    business_path = get_path_from_root("data", "raw", "Yelp Data", "business.json")
    business_data_pa = load_data_in_chunks(business_path, chunk_size)

    return business_data_pa


def get_review_df():
    review_path = get_path_from_root("data", "raw", "Yelp Data", "review.json")
    review_data_pa = load_data_in_chunks(review_path, chunk_size)

    return review_data_pa


# Function to load cleaned business data
def get_clean_business_df():
    path = get_path_from_root("data", "interim", "cleaned_business.json")
    try:
        return pd.read_json(path, lines=True)
    except Exception as e:
        logger.error(f"Error loading business data: {e}")
        return pd.DataFrame()


def get_geodata():
    path = get_path_from_root("data", "GIS Data", "export.geojson")
    try:
        return gpd.read_file(path)
    except Exception as e:
        logger.error(f"Error loading GeoJSON data: {e}")
        return gpd.GeoDataFrame()