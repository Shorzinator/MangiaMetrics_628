import logging
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pd.set_option('display.max_columns', None)

business_path = "C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\data\\raw\\business.json"
# business_df = pd.read_json(business_path, lines=True, chunksize=10000)

# Define chunk size
chunk_size = 10000  # Adjust this based on your machine's memory capability

# Initialize an empty DataFrame to hold filtered data
business_data_pa = pd.DataFrame()


# Function to process and filter each chunk
def process_business_chunk(chunk):
    # Filter for businesses in Pennsylvania (PA)
    return chunk[chunk['state'] == 'PA']


# Read and process the file in chunks
for chunk in pd.read_json(business_path, lines=True, chunksize=chunk_size, dtype={'postal_code': str}):
    filtered_chunk = process_business_chunk(chunk)
    business_data_pa = pd.concat([business_data_pa, filtered_chunk])


# Display the first few rows of the filtered DataFrame
# print(business_data_pa.head())

# Part 2
def count_categories(dataframe):
    category_counts = Counter()
    for row in dataframe['categories']:
        if row:  # Check if the category is not NaN
            categories = row.split(', ')
            category_counts.update(categories)
    return category_counts


# Count categories in the PA business data
pa_category_counts = count_categories(business_data_pa)


# Display the most common categories
# print("Most common categoris in PA:")
# for category, count in pa_category_counts.most_common(10):
#     print(f"{category}: {count}")

# Plotting the top categories
# top_categories = pa_category_counts.most_common(10)
# categories, counts = zip(*top_categories)
# plt.figure(figsize=(10, 6))
# plt.bar(categories, counts)
# plt.xticks(rotation=45)
# plt.title('Top 10 business categories in PA')
# plt.xlabel('Category')
# plt.ylabel('Count')


# plt.savefig('Top_10_businesses_in_PA.png')
# plt.show()

# Part 3
# Adjusted function to handle None values in 'categories'
def extract_restaurant_types(row):
    if row['categories'] and 'Restaurants' in row['categories']:
        # Extract and return the list of restaurant types/categories
        return [category.strip() for category in row['categories'].split(',') if category.strip() != 'Restaurants']
    return []


# Apply the function to the DataFrame
business_data_pa['restaurant_types'] = business_data_pa.apply(extract_restaurant_types, axis=1)

# Flatten the list of types and count occurrences
restaurant_type_counts = pd.Series(
    [item for sublist in business_data_pa['restaurant_types'] for item in sublist]).value_counts()

# Display the most common restaurant types
# print("Most common restaurant types in PA:")
# print(restaurant_type_counts.head(10))

# Plot the results
restaurant_type_counts.head(10).plot(kind='bar', figsize=(10, 6), title='Top 10 Restaurant Types in PA')
plt.xlabel('Restaurant Type')
plt.ylabel('Count')
# plt.savefig('Top_10_restaurant_types_in_PA.pnga')
# plt.show()


# Part 4.1

# Define function to filter specific restaurant categories
def filter_specific_categories(dataframe, category_list):
    filtered_df = dataframe[
        dataframe['restaurant_types'].apply(lambda types: any(cat in types for cat in category_list))]
    return filtered_df


# Filter for 'Italian' and 'Breakfast & Brunch' categories
italian_restaurants = filter_specific_categories(business_data_pa, ['Italian'])
breakfast_brunch_restaurants = filter_specific_categories(business_data_pa, ['Breakfast & Brunch'])


# Function to calculate basic metrics for a category
def calculate_basic_metrics(df, category_name):
    average_rating = df['stars'].mean()
    total_restaurants = len(df)
    average_review_count = df['review_count'].mean()
    print(f"Metrics for {category_name}:")
    print(f"Total Restaurants: {total_restaurants}")
    print(f"Average Rating: {average_rating:.2f}")
    print(f"Average Review Count: {average_review_count:.2f}\n")


# Calculate and display metrics for Italian and Breakfast & Brunch restaurants
calculate_basic_metrics(italian_restaurants, 'Italian')
calculate_basic_metrics(breakfast_brunch_restaurants, 'Breakfast & Brunch')
