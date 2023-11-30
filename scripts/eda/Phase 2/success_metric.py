import pandas as pd

from scripts.utility.data_loader import get_clean_business_df, get_clean_review_df


# Function to calculate the weighted rating score
def calculate_weighted_rating(df):
    max_review_count = df['review_count'].max()
    df['weighted_rating'] = (df['stars'] * df['review_count']) / max_review_count
    return df['weighted_rating']


# Function to assign sentiment scores to reviews
def assign_sentiment_scores(sentiment):
    sentiment_score = {'positive': 1, 'neutral': 0, 'negative': -1}
    return sentiment_score[sentiment]


# Function to calculate the composite success score
def calculate_success_score(df):
    df['success_score'] = (df['weighted_rating'] + df['normalized_sentiment_score']) / 2
    # Normalize the success score to be out of 5
    df['success_score'] = (df['success_score'] / df['success_score'].max()) * 5
    return df


# Function to save the results to a CSV file
def save_results(df, filepath):
    df.to_csv(filepath, index=False)
    print(f'Success scores saved to {filepath}')


# Main function to process the data
def process_data():
    # Load the data
    business_data = get_clean_business_df()
    review_data = get_clean_review_df()

    # Convert to pandas DataFrame
    business_df = pd.DataFrame(business_data)
    review_df = pd.DataFrame(review_data)

    # Merge the data on business_id
    merged_df = pd.merge(business_df, review_df, on='business_id', how='left')

    # Calculate the weighted rating score
    merged_df = calculate_weighted_rating(merged_df)

    # Assign sentiment scores
    merged_df = assign_sentiment_scores(merged_df)

    # Calculate the composite success score
    merged_df = calculate_success_score(merged_df)

    # Save the results
    save_results(merged_df[['business_id', 'name', 'success_score']], output_filepath)


# Call the main function
process_data()
