import logging
import os
from datetime import datetime

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from shapely import Point
from sklearn.linear_model import LinearRegression

from scripts.utility.path_utils import get_path_from_root

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set Pandas display option
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# Function definitions
def load_data_in_chunks(file_path, chunk_size, filter_state='PA'):
    temp_df = pd.DataFrame()
    for chunk in pd.read_json(file_path, lines=True, chunksize=chunk_size, dtype={'postal_code': str}):
        temp_df = pd.concat([temp_df, chunk[chunk['state'] == filter_state]])
    return temp_df


# Function Definitions
def load_cleaned_business_data(file_path):
    try:
        return pd.read_json(file_path, lines=True)
    except Exception as e:
        logger.error(f"Error loading business data: {e}")
        return pd.DataFrame()


def extract_restaurant_types(row):
    if pd.notna(row['categories']) and 'Restaurants' in row['categories']:
        return [category.strip() for category in row['categories'].split(',') if 'Restaurants' not in category.strip()]
    return []


def filter_specific_categories(dataframe, category_list):
    return dataframe[
        dataframe['restaurant_types'].apply(lambda types: any(cat in types for cat in category_list))]


def calculate_basic_metrics(df, category_name):
    if df.empty or 'stars' not in df.columns:
        logger.error(f"{category_name} DataFrame is empty or missing required columns")
        return

    average_rating = df['stars'].mean()
    total_restaurants = len(df)
    average_review_count = df['review_count'].mean()

    logger.info(
        f"Metrics for {category_name}: Total Restaurants: {total_restaurants}, Average Rating: {average_rating:.2f}, "
        f"Average Review Count: {average_review_count:.2f}")


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


def google_trend_analysis():
    path = get_path_from_root("data", "raw", "Google Trend Data", "multiTimeline.csv")
    df = pd.read_csv(path)

    # Convert 'Week' to datetime
    df['Week'] = pd.to_datetime(df['Week'])

    # Convert 'Week' to its corresponding ordinal value
    df['Week'] = df['Week'].map(datetime.toordinal)

    # Step 3: Fit the model
    model = LinearRegression()
    model.fit(df[['Week']], df['italian_restaurants:(Pennsylvania)'])

    # Step 4: Get the slope and intercept of the line
    slope = model.coef_
    intercept = model.intercept_

    reg_line = slope * df['Week'] + intercept

    # Step 6: Plot the data along with the regression line
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='Week', y='italian_restaurants:(Pennsylvania)', color='blue')
    plt.ylabel('Relative Search Interest since 2018')
    plt.plot(df['Week'], reg_line, color='red')
    plt.title('Regression Line of Italian Food Trend in Pennsylvania')
    plt.savefig(os.path.join(get_path_from_root("results", "eda"), "Relative_Search_Interest_since_2018.png"))
    plt.show()


def load_geojson(file_path):
    return gpd.read_file(file_path)


def plot_restaurant_density(geo_df, title, file_name):
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    geo_df.plot(ax=ax, markersize=10, color='blue', label='Italian Restaurants')
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.savefig(os.path.join(get_path_from_root("results", "eda"), file_name))
    plt.close()


def save_geospatial_data_to_csv(geo_df, yelp_data, file_name):
    # Convert Yelp data to a GeoDataFrame
    if 'latitude' in yelp_data.columns and 'longitude' in yelp_data.columns:
        buffer_radius = 0.001  # This is roughly 100 meters, adjust as needed

        # Convert Yelp data to a GeoDataFrame with a buffer
        yelp_gdf = gpd.GeoDataFrame(
            yelp_data,
            geometry=[Point(xy).buffer(buffer_radius) for xy in zip(yelp_data.longitude, yelp_data.latitude)]
        )
        yelp_gdf.set_crs(epsg=4326, inplace=True)  # Set CRS

        # Ensure the coordinate reference system matches for both GeoDataFrames
        geo_df = geo_df.to_crs(yelp_gdf.crs)

        # Perform spatial join with buffering
        merged_data = gpd.sjoin(geo_df, yelp_gdf, how="inner", predicate='intersects')

        # Check the column names and correct them
        print(merged_data.columns)

        if not merged_data.empty:
            # You'll need to replace the column names in the list below with the actual column names from merged_data
            columns_to_save = ['name_left', 'addr:street', 'addr:city', 'addr:state', 'addr:postcode', 'geometry']

            merged_data = merged_data[columns_to_save]

            # Rename columns for clarity
            merged_data.rename(columns={
                'name_left': 'name',
                'addr:street': 'address',
                'addr:city': 'city',
                'addr:state': 'state',
                'addr:postcode': 'postal_code'
                # Add any other renaming as necessary
            }, inplace=True)
            unique_columns = ['name', 'address', 'city', 'state', 'postal_code']
            merged_data.drop_duplicates(subset=unique_columns, inplace=True)

            # Save to CSV
            file_path = os.path.join(get_path_from_root("data", "interim"), file_name)
            merged_data.to_csv(file_path, index=False)
            logger.info(f"Saved merged data to {file_name}")
    else:
        logger.error("Latitude and Longitude columns are missing from the Yelp data.")


# Main function to call all tasks
def main():
    chunk_size = 10000  # Adjust based on your system's memory capability
    # Define paths to data
    # business_path = get_path_from_root("data", "raw", "Yelp Data", "business.json")
    # business_data_pa = load_data_in_chunks(business_path, chunk_size)

    cleaned_business_path = get_path_from_root("data", "interim", "cleaned_business.json")
    business_data_pa = load_data_in_chunks(cleaned_business_path, chunk_size)

    # 2
    business_data_pa['restaurant_types'] = business_data_pa.apply(extract_restaurant_types, axis=1)
    restaurant_type_counts = pd.Series(
        [item for sublist in business_data_pa['restaurant_types'] for item in sublist]).value_counts()
    plot_category_counts(restaurant_type_counts, 'Top 10 Restaurant Types in PA', 'Top_10_restaurant_types_in_PA.png')

    # 3
    # business_data_pa['restaurant_types'] = business_data_pa.apply(extract_restaurant_types, axis=1)
    # print(business_data_pa.columns)
    # italian_restaurants = filter_specific_categories(business_data_pa, ['Italian'])
    # # Ensure that 'italian_restaurants' is not empty and has the required columns
    # if italian_restaurants.empty or 'stars' not in italian_restaurants.columns:
    #     logger.error("Italian restaurants DataFrame is empty or missing 'stars' column")
    # else:
    #     calculate_basic_metrics(italian_restaurants, 'Italian')

    # 4
    # google_trend_analysis()

    # 5
    # italian_restaurants_geo = load_geojson(get_path_from_root("data", "raw", "GIS Data", "export.geojson"))
    # plot_restaurant_density(italian_restaurants_geo, 'Density of Italian Restaurants in PA',
    #                         "italian_restaurants_density_pa.png")
    # save_geospatial_data_to_csv(italian_restaurants_geo, business_data_pa, 'italian_restaurants_geospatial_data.csv')


# Call the main function
if __name__ == "__main__":
    main()
