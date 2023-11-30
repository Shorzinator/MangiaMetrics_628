import os
import pandas as pd
from textblob import TextBlob

from scripts.utility.data_loader import get_clean_business_df, get_clean_review_df
from scripts.utility.path_utils import get_path_from_root


# Function to calculate the weighted rating score
def calculate_weighted_rating(reviews, businesses):
    # Merge the reviews with the business data to get the star ratings and review counts
    merged_data = reviews.merge(businesses[['business_id', 'stars', 'review_count']], on='business_id', how='left')
    # Calculate weighted rating score for each review
    max_review_count = merged_data['review_count'].max()
    merged_data['weighted_rating'] = (merged_data['stars'] * merged_data['review_count']) / max_review_count
    return merged_data


def calculate_success_score(reviews):
    # Normalize sentiment score to be between 0 and 1
    reviews['normalized_sentiment_score'] = (reviews['sentiment'] + 1) / 2
    # Assuming the weighted_rating is already computed and merged into the reviews DataFrame
    reviews['success_score'] = (reviews['normalized_sentiment_score'] + reviews['weighted_rating']) / 2
    # Normalize the success score to be out of 5
    reviews['success_score'] = (reviews['success_score'] / reviews['success_score'].max()) * 5
    return reviews


def assign_sentiment_scores(review_df):
    sentiment_score = {'positive': 1, 'neutral': 0, 'negative': -1}
    review_df['sentiment_score'] = review_df['sentiment_category'].map(sentiment_score)
    return review_df


# Function to save the results to a CSV file
def save_results(df, filepath):
    df.to_csv(filepath, index=False)
    print(f'Success scores saved to {filepath}')


# Function to perform sentiment analysis on the text and categorize it
def perform_sentiment_analysis(text):
    # Handle missing or non-string text
    if pd.isna(text) or not isinstance(text, str):
        return 0, 'neutral'  # Neutral sentiment for missing or non-string text

    # Get the polarity score using TextBlob
    polarity = TextBlob(text).sentiment.polarity
    # Categorize the polarity into sentiment categories
    if polarity > 0:
        return polarity, 'positive'
    elif polarity < 0:
        return polarity, 'negative'
    else:
        return polarity, 'neutral'


def main():
    # Load the data
    business_df = get_clean_business_df()
    review_df = get_clean_review_df()

    # Perform sentiment analysis and categorize
    results = review_df['text'].apply(perform_sentiment_analysis)
    review_df['sentiment'] = results.apply(lambda x: x[0])
    review_df['sentiment_category'] = results.apply(lambda x: x[1])

    # Ensure the merged_data DataFrame from calculate_weighted_rating has the business name
    # Otherwise, the following line will fail because 'name' column won't exist
    merged_df = calculate_weighted_rating(review_df, business_df)

    # Assign sentiment scores based on categories
    merged_df = assign_sentiment_scores(merged_df)

    # Calculate the composite success score
    merged_df['success_score'] = calculate_success_score(merged_df)

    # Define the output filepath
    output_filename = "success_scores.csv"
    output_filepath = os.path.join(get_path_from_root("results", "eda", "Phase 2"), output_filename)

    # Save the results
    save_results(merged_df[['business_id', 'success_score']], output_filepath)


# Call the main function
if __name__ == "__main__":
    main()
