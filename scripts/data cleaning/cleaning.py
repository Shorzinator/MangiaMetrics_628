import collections
import json
import logging
import os
import re

import nltk
import pandas as pd
from nltk.corpus import stopwords

from config import BUSINESS_CLEANING_CONFIG, REVIEW_CLEANING_CONFIG
from scripts.utility.data_loader import get_business_df
from scripts.utility.path_utils import get_path_from_root

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Display all columns
pd.set_option('display.max_columns', None)

# nltk.download("stopwords")
# nltk.download("wordnet")
# nltk.download("punkt")


def get_cleaned_business_ids():
    path = get_path_from_root("data", "interim", "cleaned_business.json")
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        cleaned_business_df = pd.DataFrame(data)
        return cleaned_business_df['business_id'].unique().tolist()
    except Exception as e:
        logging.error(f"Error in get_cleaned_business_ids: {e}")
        return []


def parse_attributes(attributes):
    # Return the attributes as-is if it's a dictionary, or an empty dictionary if None
    return attributes if isinstance(attributes, dict) else {}


def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.abc.MutableMapping):
            try:
                nested_dict = json.loads(v.replace("'", "\""))
                items.extend(flatten_dict(nested_dict, new_key, sep=sep).items())
            except (json.JSONDecodeError, AttributeError):
                items.append((new_key, v))
        else:
            items.append((new_key, v))
    return dict(items)


def flatten_attributes(business_df):
    # Parse the attribute column into dictionaries
    business_df['attributes'] = business_df['attributes'].apply(parse_attributes)

    return business_df.join(pd.DataFrame([flatten_dict(row) for row in business_df['attributes']]))


def save_pretty_json(df, path):
    with open(path, 'w') as f:
        try:
            json_data = df.to_dict(orient='records')
            json.dump(json_data, f, indent=4)
        except Exception as e:
            logging.error(f"Error in save_pretty_json: {e}")
            raise


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

        business_df = flatten_attributes(business_df)

        # Save cleaned data
        path_to_save = get_path_from_root("data", "interim")
        os.makedirs(path_to_save, exist_ok=True)

        save_pretty_json(business_df, os.path.join(path_to_save, "cleaned_business.json"))
        # business_df.to_json(os.path.join(path_to_save, "cleaned_business.json"), orient='records', lines=True)

        logging.info(f"Cleaned business data saved to {path_to_save}")

    except Exception as e:
        logging.error(f"Error in clean_business: {e}")
        raise


def preprocess_text(text):
    # Remove URLs
    text = re.sub(r'http\S+', '', text)

    # Replace special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Tokenization and lowercase
    words = nltk.word_tokenize(text.lower())

    # Stopword removal
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]

    # Negation handling
    words = ['not_' + words[i + 1] if words[i] == 'not' and i + 1 < len(words) else words[i] for i in range(len(words))]

    # Lemmatization
    lemmatizer = nltk.WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    words = [lemmatizer.lemmatize(word, pos='n') for word in words]  # Lemmatize nouns
    words = [lemmatizer.lemmatize(word, pos='v') for word in words]  # Lemmatize verbs

    # Rejoin words into a string
    return " ".join(words)


def clean_reviews_chunk(chunk):
    chunk = chunk.copy()  # Create a copy of the chunk to avoid SettingWithCopyWarning

    # Filter based on business IDs from cleaned business data
    chunk = chunk[chunk['business_id'].isin(REVIEW_CLEANING_CONFIG['business_ids'])]

    # Standardize date formats and handle missing values
    chunk.loc[:, 'date'] = pd.to_datetime(chunk['date'], errors='coerce')
    chunk.dropna(subset=['review_id', 'user_id', 'business_id', 'date'], inplace=True)

    # Remove duplicates and preprocess text for sentiment analysis
    chunk.drop_duplicates(subset='review_id', inplace=True)
    chunk.loc[:, 'text'] = chunk['text'].str.lower().str.replace(r'[^\w\s]+', '')
    chunk.loc[:, 'text'] = chunk["text"].apply(lambda x: preprocess_text(x))

    return chunk


def clean_reviews():
    try:
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


def clean_trips_data():
    input_path = os.path.join(get_path_from_root("data", "raw", "Transportation Data"), "Trips_by_Distance.csv")
    output_path = get_path_from_root("data", "interim")

    # Load the dataset
    df = pd.read_csv(input_path)

    df = df[df["State Postal Code"] == "PA"]

    # Define columns to drop
    columns_to_drop = ['State FIPS', 'State Postal Code', 'Level', 'Row ID', 'Week', 'Number of Trips >=500',
                       'County FIPS']

    # Drop the unnecessary columns
    df_cleaned = df.drop(columns=columns_to_drop, axis=1)

    # Convert 'Date' to datetime, and set it as the index
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Save the cleaned dataset to a new file
    df_cleaned.to_csv(os.path.join(output_path, "cleaned_transportation.csv"), index=False)
    logger.info(f"Cleaned transportation data saved to {output_path}")


def clean_new_dp03():
    input_path = os.path.join(get_path_from_root("data", "raw", "Census Bureau Data"),
                              "DP03.csv")
    output_path = os.path.join(get_path_from_root("data", "interim"), "new_cleaned_dp03.csv")

    # Read the CSV file
    df = pd.read_csv(input_path)

    # Process initial hierarchical structure
    def count_leading_spaces(value):
        if isinstance(value, str):
            return len(value) - len(value.lstrip(' '))
        else:
            return 0

    df['IndentLevel'] = df['Label (Grouping)'].apply(count_leading_spaces)

    max_indent = df['IndentLevel'].max()
    for level in range(max_indent + 1):
        df[f'Level_{level}'] = None
        mask = df['IndentLevel'] == level
        df.loc[mask, f'Level_{level}'] = df.loc[mask, 'Label (Grouping)'].str.strip()

    for level in range(max_indent + 1):
        df[f'Level_{level}'] = df[f'Level_{level}'].ffill()

    df.drop(columns=['Label (Grouping)', 'IndentLevel'], inplace=True)

    # Update 'Level_0' to represent the hierarchy
    def update_hierarchy_column(df):
        current_path = []  # Initialize an empty list to store the current hierarchy path
        hierarchy = []  # Initialize an empty list to store the final hierarchy for each row

        for label in df['Level_0']:
            print(label)
            if label.isupper():  # Major category
                current_path = [label]  # Start a new path
                print("current path:", current_path)
            elif label.endswith(':'):  # Subcategory
                current_path.append(label)  # Append to the current path
            else:  # Continuation of the current hierarchy
                if current_path:
                    current_path[-1] = label  # Replace the last part of the current path
                else:
                    current_path.append(label)  # Start a new path if empty

            hierarchy.append(' -> '.join(current_path))
            print("hierarchy:", hierarchy)

        df['Level_0'] = hierarchy
        return df

    # df = update_hierarchy_column(df)

    # Standardize ZIP code column names
    def standardize_zip_code_columns(df):
        for col in df.columns:
            if 'ZCTA5' in col and '!!Estimate' in col:
                new_col_name = col.split()[1]  # Extracting the ZIP code
                df.rename(columns={col: new_col_name}, inplace=True)

        df.columns = [col.replace("!!Estimate", "") for col in df.columns]
        return df

    df = standardize_zip_code_columns(df)

    # Drop redundant columns
    columns_to_drop = [col for col in df.columns if 'Margin of Error' in col or 'Percent' in col]
    df.drop(columns=columns_to_drop, inplace=True)

    # Save the cleaned DataFrame
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    # clean_business()
    #
    # REVIEW_CLEANING_CONFIG['business_ids'] = get_cleaned_business_ids()
    # clean_reviews()

    clean_trips_data()
