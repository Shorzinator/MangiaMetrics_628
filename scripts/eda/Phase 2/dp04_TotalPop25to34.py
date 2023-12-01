import os

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

from scripts.utility.path_utils import get_path_from_root


def main():
    # Define file paths (please adjust these paths as per your directory structure)
    shp_path = os.path.join(get_path_from_root("data", "raw", "shape_files_for_pa"), "PA_ZipCode_data.shp")
    demographic_path = os.path.join(get_path_from_root("data", "final"), "final_dp05.csv")
    gis_path = os.path.join(get_path_from_root("data", "interim"), "flattened_gis.csv")

    # Load shapefile, demographic data, and GIS data
    pa_shapefile = gpd.read_file(shp_path)
    demographic_data = pd.read_csv(demographic_path)
    gis_data = pd.read_csv(gis_path)

    # Convert GIS data to a GeoDataFrame
    gdf_gis = gpd.GeoDataFrame(gis_data, geometry=gpd.points_from_xy(gis_data.longitude, gis_data.latitude))

    # Ensure the ZIP Code columns in demographic data and shapefile are of the same data type
    demographic_data['ZIP Code'] = demographic_data['ZIP Code'].astype(str)
    pa_shapefile['ZIP_CODE'] = pa_shapefile['ZIP_CODE'].astype(str)

    # Merge the shapefile with the demographic data
    merged_data = pa_shapefile.merge(demographic_data, left_on='ZIP_CODE', right_on='ZIP Code')

    # Create the choropleth map
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    merged_data.plot(column='Sex and Age - Total population', ax=ax, legend=True, cmap='YlOrRd')

    # Overlay GIS data (points)
    gdf_gis.plot(ax=ax, marker='o', color='blue', markersize=5)

    # Adding map titles and labels
    plt.title('Pennsylvania ZIP Codes - Total Population Aged 25 to 34 Years with GIS Points')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # Show the map
    plt.show()


if __name__ == "__main__":
    main()
