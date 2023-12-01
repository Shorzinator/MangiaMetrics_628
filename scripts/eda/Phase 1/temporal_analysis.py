import json
import os
from datetime import datetime, time

import matplotlib.pyplot as plt
import pandas as pd

from scripts.utility.path_utils import get_path_from_root


def parse_hours(hours_data):
    """
    Convert hours from JSON format into a more usable structure.
    Handles both string and dictionary input.
    """
    if not hours_data or pd.isnull(hours_data):
        return {}

    if isinstance(hours_data, str):
        try:
            hours_dict = json.loads(hours_data)
        except json.JSONDecodeError:
            return {}
    elif isinstance(hours_data, dict):
        hours_dict = hours_data
    else:
        return {}

    parsed_hours = {}
    for day, hours in hours_dict.items():
        if hours:
            open_time, close_time = hours.split('-')
            parsed_hours[day] = {
                'open': datetime.strptime(open_time, '%H:%M').time(),
                'close': datetime.strptime(close_time, '%H:%M').time()
            }
    return parsed_hours


def is_within_business_hours(row):
    hours = row['parsed_hours'].get(row['day_of_week'], {})
    if hours:
        review_datetime = datetime.combine(row['date'].date(), time(hour=row['hour']))
        open_datetime = datetime.combine(row['date'].date(), hours['open'])
        close_datetime = datetime.combine(row['date'].date(), hours['close'])
        return open_datetime <= review_datetime <= close_datetime
    return False


def temporal_analysis(business_df, review_df, transportation_df, path_to_save):
    """
    Perform temporal analysis on the dataset to find the busiest times for businesses.
    """
    os.makedirs(path_to_save, exist_ok=True)

    # Parsing business hours
    business_df['parsed_hours'] = business_df['hours'].apply(parse_hours)

    # Merging reviews with business hours
    merged_df = review_df.merge(business_df[['business_id', 'parsed_hours']], on='business_id', how='left')

    # Converting review 'date' to datetime
    merged_df['date'] = pd.to_datetime(merged_df['date'])

    # Extracting day of week and hour from review date
    merged_df['day_of_week'] = merged_df['date'].dt.day_name()
    merged_df['hour'] = merged_df['date'].dt.hour

    # For each review, check if it falls within the business hours
    merged_df['within_business_hours'] = merged_df.apply(is_within_business_hours, axis=1)

    # Aggregate counts of reviews within business hours
    within_hours_review_count = merged_df.groupby(['day_of_week', 'within_business_hours']).size().unstack(fill_value=0)

    # Plotting
    within_hours_review_count.plot(kind='bar', stacked=True, figsize=(14, 7))
    plt.title('Number of Reviews Within Business Hours by Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Reviews')
    plt.legend(title='Within Business Hours', labels=['No', 'Yes'])
    plt.tight_layout()
    plt.savefig(os.path.join(path_to_save, 'reviews_within_business_hours.png'))
    plt.show()


def main():
    # Paths for the datasets
    file_paths = {
        'business_json': get_path_from_root("data", "interim", "cleaned_business.json"),
        'review_json': get_path_from_root("data", "interim", "cleaned_reviews.json"),
        'transportation_csv': get_path_from_root("data", "interim", "cleaned_transportation.csv")
    }

    # Loading the datasets
    business_df = pd.read_json(file_paths['business_json'], lines=True)
    review_df = pd.read_json(file_paths['review_json'], lines=True)
    transportation_df = pd.read_csv(file_paths['transportation_csv'])

    # Directory to save plots
    path_to_save = get_path_from_root("results", "eda")

    # Performing temporal analysis
    temporal_analysis(business_df, review_df, transportation_df, path_to_save)


if __name__ == "__main__":
    main()
