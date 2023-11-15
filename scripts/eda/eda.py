import logging
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set Pandas display option
pd.set_option('display.max_columns', None)

# Define paths to data
business_path = "C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\data\\raw\\business.json"

# Initialize DataFrame to hold business data
business_data_pa = pd.DataFrame()


# Function definitions
def load_data_in_chunks(file_path, chunk_size, filter_state='PA'):
    temp_df = pd.DataFrame()
    for chunk in pd.read_json(file_path, lines=True, chunksize=chunk_size, dtype={'postal_code': str}):
        temp_df = pd.concat([temp_df, chunk[chunk['state'] == filter_state]])
    return temp_df


def count_categories(dataframe):
    category_counts = Counter()
    for row in dataframe['categories']:
        if row:
            categories = row.split(', ')
            category_counts.update(categories)
    return category_counts


def extract_restaurant_types(row):
    if row['categories'] and 'Restaurants' in row['categories']:
        return [category.strip() for category in row['categories'].split(',') if category.strip() != 'Restaurants']
    return []


def filter_specific_categories(dataframe, category_list):
    return dataframe[
        dataframe['restaurant_types'].apply(lambda types: any(cat in types for cat in category_list))]


def calculate_basic_metrics(df, category_name):
    average_rating = df['stars'].mean()
    total_restaurants = len(df)
    average_review_count = df['review_count'].mean()
    print(f"Metrics for {category_name}:")
    print(f"Total Restaurants: {total_restaurants}")
    print(f"Average Rating: {average_rating:.2f}")
    print(f"Average Review Count: {average_review_count:.2f}")


def plot_category_counts(counter, title, file_name):
    # Convert the Counter object to a Panda Series
    series = pd.Series(counter)
    top_categories = series.nlargest(10)
    top_categories.plot(kind='bar', figsize=(10, 6))
    plt.xticks(rotation=45)
    plt.title(title)
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.tight_layout()  # Adjust layout to fit labels
    plt.savefig(file_name)
    plt.close()


# Main function to call all tasks
def main():
    chunk_size = 10000  # Adjust based on your system's memory capability
    business_data_pa = load_data_in_chunks(business_path, chunk_size)

    # Uncomment the following lines to perform the respective tasks
    pa_category_counts = count_categories(business_data_pa)
    plot_category_counts(pa_category_counts, 'Top 10 Business Categories in PA', 'Top_10_business_categories_in_PA.png')

    business_data_pa['restaurant_types'] = business_data_pa.apply(extract_restaurant_types, axis=1)
    restaurant_type_counts = pd.Series(
        [item for sublist in business_data_pa['restaurant_types'] for item in sublist]).value_counts()
    plot_category_counts(restaurant_type_counts, 'Top 10 Restaurant Types in PA', 'Top_10_restaurant_types_in_PA.png')

    italian_restaurants = filter_specific_categories(business_data_pa, ['Italian'])
    breakfast_brunch_restaurants = filter_specific_categories(business_data_pa, ['Breakfast & Brunch'])
    calculate_basic_metrics(italian_restaurants, 'Italian')
    calculate_basic_metrics(breakfast_brunch_restaurants, 'Breakfast & Brunch')


# Call the main function
if __name__ == "__main__":
    main()
