from scripts.utility.data_loader import get_business_df
from scripts.utility.path_utils import get_path_from_root


def clean_business():
    business_df = get_business_df()

    # Filter for restaurants in Pennsylvania
    business_df = business_df[business_df['categories'].str.contains('Restaurants', na=False)]
    business_df = business_df[business_df['state'] == 'PA']

    # Remove businesses that are closed
    business_df = business_df[business_df["is_open"] == 1]

    # Remove duplicate entries based on business_id
    business_df = business_df.drop_duplicates(subset="business_id")

    # Normalize text in categories
    business_df["city"] = business_df["city"].str.lower()
    business_df["categories"] = business_df["categories"].str.lower()

    # Drop rows with missing categories
    business_df = business_df.dropna(subset=["categories"])

    path_to_save = get_path_from_root("data", "interim", "cleaned_business.json")
    business_df.to_json(path_to_save)

    print(f"Cleaned data saved to {path_to_save}")


# Define a function to clean each chunk
def clean_reviews_chunk(chunk):
    # Filter based on cleaned business data (assuming you have a list of relevant business IDs)
    chunk = chunk[chunk['business_id'].isin(business_ids)]

    # Handle missing values or drop duplicates as needed
    chunk.dropna(subset=['review_id', 'user_id', 'business_id'], inplace=True)
    chunk.drop_duplicates(subset='review_id', inplace=True)

    # Standardize date formats
    chunk['date'] = pd.to_datetime(chunk['date']).dt.strftime('%Y-%m-%d')

    return chunk


def clean_reviews():
    # Process the review.json file in chunks and append to a new dataframe
    cleaned_reviews_df = pd.DataFrame()
    for chunk in pd.read_json('review.json', lines=True, chunksize=10000):
        cleaned_chunk = clean_reviews_chunk(chunk)
        cleaned_reviews_df = pd.concat([cleaned_reviews_df, cleaned_chunk])


clean_business()
