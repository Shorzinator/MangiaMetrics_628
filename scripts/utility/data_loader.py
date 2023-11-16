import pandas as pd

from scripts.eda.eda import load_data_in_chunks
from scripts.utility.path_utils import get_path_from_root

chunk_size = 10000  # Adjust based on system's memory capability


def get_business_df():
    # Define paths to data
    business_path = get_path_from_root("data", "raw", "Yelp Data", "business.json")
    business_data_pa = load_data_in_chunks(business_path, chunk_size)

    return business_data_pa


def get_review_df():
    review_path = get_path_from_root("data", "raw", "Yelp Data", "review.json")
    review_data_pa = load_data_in_chunks(review_path, chunk_size)

    return review_data_pa

