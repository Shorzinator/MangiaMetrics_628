import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

BUSINESS_CLEANING_CONFIG = {
    'category_filter': 'Italian',
    'state_filter': 'PA',
    # Add more configurable parameters as needed
}

# Configurations for cleaning review data
REVIEW_CLEANING_CONFIG = {
    'chunk_size': 10000,
    'business_ids': [],  # This will be populated dynamically
    # Other configurations...
}
