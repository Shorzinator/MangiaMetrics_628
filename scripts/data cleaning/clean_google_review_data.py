import os
import re
from datetime import datetime

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm

from scripts.utility.path_utils import get_path_from_root


# Ensure required NLTK data is downloaded
# nltk.download("stopwords")
# nltk.download("wordnet")
# nltk.download("punkt")


def preprocess_text(text):
    # Check if the text is not a string
    if not isinstance(text, str):
        return ""

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
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    words = [lemmatizer.lemmatize(word, pos='n') for word in words]  # Lemmatize nouns
    words = [lemmatizer.lemmatize(word, pos='v') for word in words]  # Lemmatize verbs

    # Rejoin words into a string
    return " ".join(words)


def unix_to_datetime(unix_time):
    """ Convert Unix timestamp to datetime """
    try:
        # Convert Unix timestamp to datetime, assuming the timestamp is in milliseconds
        return datetime.utcfromtimestamp(int(unix_time) / 1000.0)
    except (ValueError, TypeError):
        # Return None or a default datetime in case of an error
        return None


def get_cleaned_gmap_ids():
    """
    Extracts a list of unique gmap_ids from the cleaned Google Maps business data.

    Parameters:
    cleaned_business_data_path (str): Path to the cleaned Google Maps business data CSV file.

    Returns:
    list: A list of unique gmap_ids.
    """
    try:
        # Load the cleaned business data
        cleaned_business_data_path = get_path_from_root("data", "interim", "cleaned_google_business.csv")
        business_df = pd.read_csv(cleaned_business_data_path)

        # Extract and return the unique gmap_ids
        ids = business_df['gmap_id'].unique().tolist()
        return ids
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def process_google_reviews_chunk(chunk):
    # Apply preprocessing to each chunk
    chunk['datetime'] = chunk['time'].apply(unix_to_datetime)
    chunk = chunk.dropna(subset=['datetime'])
    chunk['date'] = chunk['datetime'].dt.date
    chunk['time'] = chunk['datetime'].dt.strftime('%H:%M:%S')
    chunk.drop(['datetime'], axis=1, inplace=True)
    chunk['text'] = chunk['text'].apply(preprocess_text)
    return chunk


def clean_google_reviews(file_path_google, chunk_size=10000):

    # Convert to DataFrame
    concatenated_df = pd.DataFrame()

    with open(file_path_google, 'r') as file:
        # Calculate total number of chunks (approximation)
        total_size = os.path.getsize(file_path_google)
        total_chunks = total_size // (chunk_size * 100)  # Adjust factor based on average line length

        for chunk in tqdm(pd.read_json(file, lines=True, chunksize=chunk_size), total=total_chunks):
            processed_chunk = process_google_reviews_chunk(chunk)
            concatenated_df = pd.concat([concatenated_df, processed_chunk], ignore_index=True)

    # Drop columns that are not needed and rename columns
    concatenated_df.drop(['name', 'pics', 'resp'], axis=1, inplace=True)
    concatenated_df.rename(columns={'rating': 'stars'}, inplace=True)

    # Save the cleaned Google Maps review data to CSV
    path = get_path_from_root("data", "interim")
    concatenated_df.to_csv(os.path.join(path, 'cleaned_google_reviews.csv'), index=False)

    # return concatenated_df


# Usage
file_path_google = 'C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\data\\raw\\Google Maps Data\\review_PA.json'
clean_google_reviews(file_path_google)
