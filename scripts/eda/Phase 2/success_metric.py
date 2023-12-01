import os

import pandas as pd
from textblob import TextBlob

from scripts.utility.path_utils import get_path_from_root

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


# Function to calculate the weighted rating score
def calculate_weighted_rating(merged_data):
    # Calculate weighted rating score for each review
    max_review_count = merged_data['review_count'].max()
    merged_data['weighted_rating'] = (merged_data['stars_review'] * merged_data['review_count']) / max_review_count
    return merged_data


# Function to perform sentiment analysis on the text and categorize it
def perform_sentiment_analysis(text):
    # Handle missing or non-string text
    if pd.isna(text) or not isinstance(text, str):
        return 0, 'neutral'  # Neutral sentiment for missing or non-string text

    # Get the polarity score using TextBlob
    polarity = TextBlob(text).sentiment.polarity
    # Categorize the polarity into sentiment categories
    if polarity > 0.2:
        return polarity, 'positive'
    elif polarity < -0.2:
        return polarity, 'negative'
    else:
        return polarity, 'neutral'


def main():
    path = os.path.join(get_path_from_root("data", "interim"), "business_x_review.csv")
    merged_data = pd.read_csv(path)

    # Merging and calculating the weighted rating
    merged_df = calculate_weighted_rating(merged_data)

    # Normalizing the sentiment score
    sentiment_score = {'positive': 1, 'neutral': 0, 'negative': -1}
    merged_df['sentiment_score'] = merged_df['sentiment_category'].map(sentiment_score)
    max_sentiment_score = merged_df['sentiment_score'].max()
    min_sentiment_score = merged_df['sentiment_score'].min()
    merged_df['normalized_sentiment_score'] = (merged_df['sentiment_score'] - min_sentiment_score) / (
            max_sentiment_score - min_sentiment_score)

    # Normalizing the weighted rating
    max_weighted_rating = merged_df['weighted_rating'].max()
    merged_df['normalized_weighted_rating'] = merged_df['weighted_rating'] / max_weighted_rating

    # Calculating the success score
    merged_df['success_score'] = (merged_df['normalized_sentiment_score'] + merged_df['normalized_weighted_rating']) / 2
    # Normalize the success score to be out of 5
    merged_df['success_score'] = (merged_df['success_score'] / merged_df['success_score'].max()) * 5
    merged_data.to_csv(os.path.join(get_path_from_root("data", "interim"), "business_x_review.csv"),
                       index=False)

    # print(merged_df.head(10))


if __name__ == "__main__":
    main()
