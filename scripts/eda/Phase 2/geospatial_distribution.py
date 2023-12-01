import matplotlib.pyplot as plt

from scripts.utility.data_loader import get_clean_business_df, get_geodata


# Define function to plot the restaurants' distribution
def plot_restaurant_distribution(restaurants_gdf, geo_data, title, file_name):
    fig, ax = plt.subplots(figsize=(10, 10))

    # Check if geo_data contains points or boundaries
    if 'geometry' in geo_data.columns:
        # Plot the PA map as a base
        geo_data.plot(ax=ax, color='lightgrey', edgecolor='black')

    # Plot the Italian restaurants
    restaurants_gdf.plot(ax=ax, markersize=50, color='red', label='Italian Restaurants')

    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.savefig(file_name)
    plt.show()


# Main function to execute the script
def main():
    # Load the business data
    business_df = get_clean_business_df()

    # Load the geojson data
    geo_df = get_geodata()

    # Plotting the restaurant distribution
    plot_restaurant_distribution(business_df, geo_df, 'Distribution of Italian Restaurants in PA',
                                 'italian_restaurants_distribution_pa.png')


if __name__ == "__main__":
    main()
