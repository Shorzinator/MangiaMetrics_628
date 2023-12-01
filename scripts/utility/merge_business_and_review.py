import os

import pandas as pd
from textblob import TextBlob

from scripts.utility.path_utils import get_path_from_root

pd.set_option("display.max_rows", 200)
pd.set_option("display.max_columns", 200)

# Reload the business and review data as the previous code execution state was reset
business_filepath = 'C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\data\\interim\\flattened_business.csv'
review_filepath = 'C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\data\\interim\\flattened_review.csv'

# Reading the CSV files
business_df = pd.read_csv(business_filepath)
review_df = pd.read_csv(review_filepath)

# Merging the reviews with the business data
# Keeping only relevant columns from business data for the merge
merged_data = review_df.merge(
    business_df[['business_id', 'stars', 'review_count']],
    on='business_id',
    how='left',
    suffixes=('_review', '_business')
)


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


# Perform sentiment analysis and categorize
results = merged_data['text'].apply(perform_sentiment_analysis)
merged_data['sentiment'] = results.apply(lambda x: x[0])
merged_data['sentiment_category'] = results.apply(lambda x: x[1])

# Displaying the first few rows of the merged dataframe to check the merge and sentiment analysis
merged_data.to_csv(os.path.join(get_path_from_root("data", "interim"), "business_x_review.csv"),
                   index=False)
# print(merged_data.head())
