import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster

# Replace these with the paths to your files
path_to_demographic_data = 'path_to_your_final_dp05.csv'
path_to_restaurant_data = 'path_to_your_flattened_gis.csv'
path_to_pa_shapefile = 'path_to_your_pennsylvania_administrative.shp'

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

# Create the interactive map using Folium, centered on Pennsylvania
m = folium.Map(location=[40.90, -77.84], zoom_start=7)

# Plot the shapefile as the base layer
folium.GeoJson(
    gdf_pa_shapefile.__geo_interface__,
    name='PA Administrative Boundaries'
).add_to(m)

# Add a marker cluster to hold the restaurant points
marker_cluster = MarkerCluster().add_to(m)

# Add each restaurant to the marker cluster
for idx, row in gdf_restaurants.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['name']  # Replace 'name' with the actual restaurant name column
    ).add_to(marker_cluster)

# Save the interactive map to an HTML file
output_html = 'path_to_save_your_pa_italian_restaurants_map.html'
m.save(output_html)

# This path is where the map is saved, you can open this file in a web browser
print(f"Map saved to {output_html}")
