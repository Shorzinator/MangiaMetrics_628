import pandas as pd

from config import BUSINESS_CLEANING_CONFIG, REVIEW_CLEANING_CONFIG
from scripts.utility.data_loader import get_business_df
from scripts.utility.path_utils import get_path_from_root
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_cleaned_business_ids():
    path = get_path_from_root("data", "interim", "cleaned_business.json")
    cleaned_business_df = pd.read_json(path, lines=True)
    return cleaned_business_df['business_id'].unique().tolist()


def clean_business():
    try:
        business_df = get_business_df()

        # Filter for restaurants in Pennsylvania
        business_df = business_df[
            business_df['categories'].str.contains(BUSINESS_CLEANING_CONFIG['category_filter'], case=False, na=False)]
        business_df = business_df[business_df['state'] == BUSINESS_CLEANING_CONFIG['state_filter']]

        # Remove businesses that are closed
        business_df = business_df[business_df["is_open"] == 1]

        # Remove duplicate entries based on business_id
        business_df = business_df.drop_duplicates(subset="business_id")

        # Normalize text fields
        business_df["city"] = business_df["city"].str.lower()
        business_df["categories"] = business_df["categories"].str.lower()
        business_df["address"] = business_df["address"].str.lower()

        # Handle missing values
        business_df.dropna(subset=["latitude", "longitude", "stars", "review_count", "categories"], inplace=True)

        # Data Type Correction
        business_df["stars"] = pd.to_numeric(business_df["stars"], errors='coerce')
        business_df["review_count"] = pd.to_numeric(business_df["review_count"], errors='coerce')

        # Error Checking
        business_df = business_df[(business_df["stars"] >= 0) & (business_df["review_count"] >= 0)]
        business_df = business_df[
            (business_df["latitude"].between(-90, 90)) & (business_df["longitude"].between(-180, 180))]

        # Save cleaned data
        path_to_save = get_path_from_root("data", "interim", "cleaned_business.json")
        business_df.to_json(path_to_save, orient='records', lines=True)

        logging.info(f"Cleaned data saved to {path_to_save}")

    except Exception as e:
        logging.error(f"Error in clean_business: {e}")


def clean_reviews_chunk(chunk):
    # Filter based on business IDs from cleaned business data
    chunk = chunk[chunk['business_id'].isin(REVIEW_CLEANING_CONFIG['business_ids'])]

    # Standardize date formats and handle missing values
    chunk['date'] = pd.to_datetime(chunk['date'], errors='coerce')
    chunk.dropna(subset=['review_id', 'user_id', 'business_id', 'date'], inplace=True)

    # Remove duplicates and preprocess text for sentiment analysis
    chunk.drop_duplicates(subset='review_id', inplace=True)
    chunk['text'] = chunk['text'].str.lower().str.replace(r'[^\w\s]+', '')

    return chunk


def clean_reviews():
    try:
        cleaned_reviews_df = pd.DataFrame()
        chunks = []

        for chunk in pd.read_json(get_path_from_root("data", "raw", "Yelp Data", "review.json"), lines=True,
                                  chunksize=REVIEW_CLEANING_CONFIG['chunk_size']):
            cleaned_chunk = clean_reviews_chunk(chunk)
            chunks.append(cleaned_chunk)

        cleaned_reviews_df = pd.concat(chunks)

        # Save cleaned data
        path_to_save = get_path_from_root("data", "interim", "cleaned_reviews.json")
        cleaned_reviews_df.to_json(path_to_save, orient='records', lines=True)

        logging.info(f"Cleaned review data saved to {path_to_save}")

    except Exception as e:
        logging.error(f"Error in clean_reviews: {e}")


if __name__ == "__main__":
    clean_business()

    REVIEW_CLEANING_CONFIG['business_ids'] = get_cleaned_business_ids()
    clean_reviews()
