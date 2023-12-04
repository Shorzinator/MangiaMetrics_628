import os
import folium
import geopandas as gpd
import pandas as pd
from folium.plugins import MarkerCluster
from scripts.utility.path_utils import get_path_from_root
from tqdm import tqdm

# File paths
path_to_demographic_data = os.path.join(get_path_from_root("data", "interim"), "composite_metric.csv")
path_to_restaurant_data = os.path.join(get_path_from_root("data", "interim"), "flattened_gis.csv")
path_to_pa_shapefile = os.path.join(get_path_from_root("data", "raw", "shape_files_for_pa"), "PA_ZipCode_data.shp")

# Load the demographic data
demographic_data = pd.read_csv(path_to_demographic_data)

# Load the restaurant data
restaurant_data = pd.read_csv(path_to_restaurant_data)

# Convert restaurant data to a GeoDataFrame
gdf_restaurants = gpd.GeoDataFrame(
    restaurant_data,
    geometry=gpd.points_from_xy(restaurant_data.longitude, restaurant_data.latitude),
    crs="EPSG:4326"  # Setting WGS 84 coordinate reference system
)

# Load the Pennsylvania shapefiles
gdf_pa_shapefile = gpd.read_file(path_to_pa_shapefile)

# Ensure both ZIP_CODE columns are of the same type, e.g., convert both to string
demographic_data['ZIP_CODE'] = demographic_data['ZIP_CODE'].astype(str)
gdf_pa_shapefile['ZIP_CODE'] = gdf_pa_shapefile['ZIP_CODE'].astype(str)

# Merge the demographic data with the Pennsylvania shapefile
# Replace 'ZIP_CODE' with the actual common key column name
gdf_pa_demographic = gdf_pa_shapefile.merge(demographic_data, left_on='ZIP_CODE', right_on='ZIP_CODE')

# Create the interactive map using Folium, centered on Pennsylvania
m = folium.Map(location=[40.90, -77.84], zoom_start=7)

# Plot demographic data as a Choropleth layer
# Replace 'Median_Income' with the actual demographic column you want to visualize
demographic_features = ['Composite_Metric']

for feature in tqdm(demographic_features, desc="Creating choropleth layers"):
    layer = folium.FeatureGroup(name=feature)
    folium.Choropleth(
        geo_data=gdf_pa_demographic,
        data=gdf_pa_demographic,
        columns=['ZIP_CODE', feature],
        key_on='feature.properties.ZIP_CODE',
        fill_color='PuBuGn',
        fill_opacity=0.8,
        line_opacity=0.2,
        legend_name="Italian Restaurant Success Index"
    ).add_to(m)
    layer.add_to(m)

# Add a marker cluster for restaurant points
marker_cluster = MarkerCluster().add_to(m)

# for idx, row in gdf_restaurants.iterrows():
#     folium.Marker(
#         location=[row['latitude'], row['longitude']],
#         popup=row['name']  # Replace 'name' with the actual restaurant name column
#     ).add_to(marker_cluster)

# Add each restaurant to the marker cluster
for idx, row in gdf_restaurants.iterrows():
    # Create a string with the demographic information
    popup_content = f"""
        <strong>ZIP Code:</strong> {row['ZIP_CODE']}<br>
        <strong>Name:</strong> {row['name']}<br>
        <strong>County:</strong> {row['county']}<br>

        """

    # Create a popup
    popup = folium.Popup(popup_content, max_width=300)

    # Get the centroid of the area
    centroid = row['geometry'].centroid

    # Create an invisible marker and add it to the map
    folium.Marker(
        location=[centroid.y, centroid.x],
        icon=folium.Icon(icon_color='rgba(0,0,0,0)'),  # Invisible icon
        popup=popup
    ).add_to(marker_cluster)

# Add Layer Control to switch between choropleth layers
folium.LayerControl().add_to(m)

# Save the interactive map to an HTML file
output_html = os.path.join(get_path_from_root("results", "eda", "Phase 2"), "interactive_map_success_index_test.html")
m.save(output_html)

# Print the path where the map is saved
print(f"Map saved to {output_html}")
