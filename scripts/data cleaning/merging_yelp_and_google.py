import re

import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


# Function to perform fuzzy matching
def fuzzy_match(x, choices, scorer, cutoff):
    match, score = process.extractOne(x, choices, scorer=scorer)
    return match if score >= cutoff else None


def normalize_and_clean(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# Load datasets
yelp_business_path = 'path_to_yelp_business.csv'
google_business_path = 'path_to_google_business.csv'
yelp_review_path = 'path_to_yelp_review.csv'
google_review_path = 'path_to_google_review.csv'

yelp_business_df = pd.read_csv(yelp_business_path)
google_business_df = pd.read_csv(google_business_path)
yelp_review_df = pd.read_csv(yelp_review_path)
google_review_df = pd.read_csv(google_review_path)

# Apply normalization and cleaning to business names and addresses
yelp_business_df['name'] = yelp_business_df['name'].apply(normalize_and_clean)
yelp_business_df['address'] = yelp_business_df['address'].apply(normalize_and_clean)
yelp_business_df['city'] = yelp_business_df['city'].apply(normalize_and_clean)
yelp_business_df['ZIP Code'] = yelp_business_df['ZIP Code'].apply(normalize_and_clean)

google_business_df['name'] = google_business_df['name'].apply(normalize_and_clean)
google_business_df['city'] = google_business_df['city'].apply(normalize_and_clean)
google_business_df['ZIP Code'] = google_business_df['ZIP Code'].apply(normalize_and_clean)

# Fuzzy matching businesses
# Note: Adjust 'scorer' and 'cutoff' based on desired accuracy
yelp_business_df['matched_gmap_id'] = yelp_business_df['name'].apply(
    lambda x: fuzzy_match(x, google_business_df['name'].tolist(), fuzz.token_sort_ratio, 70)
)

# Map the matched name to its gmap_id in Google business data
mapping_df = yelp_business_df[['business_id', 'matched_gmap_id']]
mapping_df = mapping_df.merge(google_business_df[['name', 'gmap_id']], left_on='matched_gmap_id', right_on='name', how='left')
mapping_df = mapping_df[['business_id', 'gmap_id']].rename(columns={'gmap_id': 'matched_gmap_id'})
mapping_df = mapping_df.dropna()


# Combine both review datasets
combined_review_df = pd.concat([yelp_review_df, google_review_df], ignore_index=True)

# Drop duplicates and unnecessary columns
combined_review_df.drop_duplicates(subset=['review_id'], inplace=True)
combined_review_df.drop(['matched_gmap_id'], axis=1, inplace=True)

# Save the combined review dataset
combined_review_df.to_csv('combined_reviews.csv', index=False)
