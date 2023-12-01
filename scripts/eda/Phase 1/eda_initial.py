import logging

import matplotlib.pyplot as plt

from scripts.utility.data_loader import get_clean_business_df, get_geodata

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def plot_category_counts(business_data, title, file_name):
    # Assuming 'business_data' has a column 'categories' which includes 'Italian'
    category_counts = business_data['categories'].value_counts()
    category_counts.plot(kind='bar', figsize=(10, 6))
    plt.xticks(rotation=45)
    plt.title(title)
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(file_name)
    plt.close()


def plot_restaurant_density(geo_df, title, file_name):
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    geo_df.plot(ax=ax, color='blue', label='Italian Restaurants')
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.savefig(file_name)
    plt.close()


def main():
    business_data = get_clean_business_df()
    geo_data = get_geodata()

    if not business_data.empty:
        plot_category_counts(business_data, 'Category Counts of Italian Restaurants in PA', 'category_counts.png')

    if not geo_data.empty:
        plot_restaurant_density(geo_data, 'Density of Italian Restaurants in PA', 'restaurant_density.png')
    else:
        logger.error("Data loading failed.")


if __name__ == "__main__":
    main()
