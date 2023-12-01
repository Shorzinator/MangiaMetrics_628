import os

import folium
import geopandas as gpd
import pandas as pd
from folium.plugins import MarkerCluster

from scripts.utility.path_utils import get_path_from_root


def load_data(csv_path, shp_path):
    # Load CSV and shapefile data
    csv_data = pd.read_csv(csv_path)
    shp_data = gpd.read_file(shp_path)
    return csv_data, shp_data


def convert_to_geodf(df, lon_col, lat_col):
    # Convert DataFrame to GeoDataFrame
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[lon_col], df[lat_col]))
    return gdf


def create_map(gdf, shp_data, merge_col_shp, merge_col_csv):
    # Convert the merge columns to strings to ensure matching data types
    gdf[merge_col_csv] = gdf[merge_col_csv].astype(str)
    shp_data[merge_col_shp] = shp_data[merge_col_shp].astype(str)

    # Merge GeoDataFrame with shapefile data on specified columns
    merged_gdf = gdf.merge(shp_data, left_on=merge_col_csv, right_on=merge_col_shp)

    # Set the CRS for merged_gdf to WGS 84 (EPSG:4326)
    merged_gdf.set_crs("EPSG:4326", inplace=True)

    # Create a base map
    m = folium.Map(location=[40.90, -77.84], zoom_start=7)
    return m, merged_gdf


def add_choropleth(m, gdf, data_col, key_on, fill_color='YlOrRd'):
    # Add choropleth layer
    folium.Choropleth(
        geo_data=gdf,
        name='choropleth',
        data=gdf,
        columns=[key_on, data_col],
        key_on='feature.properties.' + key_on,
        fill_color=fill_color,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=data_col
    ).add_to(m)
    return m


def add_markers(m, gdf, popup_col='name'):
    # Add marker cluster
    marker_cluster = MarkerCluster().add_to(m)
    for idx, row in gdf.iterrows():
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=row[popup_col]
        ).add_to(marker_cluster)
    return m


def save_map(m, file_path):
    # Save map to HTML file
    m.save(file_path)


def main():
    # Define file paths
    csv_path = os.path.join(get_path_from_root("data", "interim"), "flattened_gis.csv")
    shp_path = os.path.join(get_path_from_root("data", "raw", "shape_files_for_pa"), "PA_ZipCode_data.shp")
    demographic_path = os.path.join(get_path_from_root("data", "final"), "final_dp05.csv")

    # Load data
    restaurant_data, pa_shapefile = load_data(csv_path, shp_path)
    demographic_data, _ = load_data(demographic_path, shp_path)

    # Convert restaurant data to GeoDataFrame
    gdf_restaurants = convert_to_geodf(restaurant_data, 'longitude', 'latitude')

    # Create map and merge data
    m, merged_gdf = create_map(gdf_restaurants, demographic_data, 'ZIP Code', 'addr:postcode')

    # Add demographic data as a choropleth layer
    # Replace 'Total population' with the column you want to visualize from demographic_data
    m = add_choropleth(m, merged_gdf, 'Sex and Age - Total population',
                       'ZIP Code')  # Adjust the column name accordingly

    # Add restaurant markers
    m = add_markers(m, gdf_restaurants, 'name')

    # Save the interactive map
    output_html = 'dp04_chloropleth.html'
    save_map(m, output_html)

    # Print the output path
    print(f"Map saved to {output_html}")


if __name__ == "__main__":
    main()
