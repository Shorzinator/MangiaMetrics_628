import os

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

from scripts.utility.path_utils import get_path_from_root


def create_chloropleth(gis_data, demographic_data, pa_shapefile, factor, filenames):
    # Convert GIS data to a GeoDataFrame
    gdf_gis = gpd.GeoDataFrame(gis_data, geometry=gpd.points_from_xy(gis_data.longitude, gis_data.latitude))

    # Ensure the ZIP Code columns in demographic data and shapefile are of the same data type
    demographic_data['ZIP Code'] = demographic_data['ZIP Code'].astype(str)
    pa_shapefile['ZIP_CODE'] = pa_shapefile['ZIP_CODE'].astype(str)

    # Merge the shapefile with the demographic data
    merged_data = pa_shapefile.merge(demographic_data, left_on='ZIP_CODE', right_on='ZIP Code')

    # Create the choropleth map
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    merged_data.plot(column=factor, ax=ax, legend=True, cmap='YlOrRd')

    # Overlay GIS data (points)
    gdf_gis.plot(ax=ax, marker='o', color='blue', markersize=5)

    # Adding map titles and labels
    plt.title(f'{factor} \n with Restaurant Density')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # Show the map
    output_path = os.path.join(get_path_from_root("results", "eda", "Phase 2", "DP03_analysis"),
                               f"dp03_{filenames}.png")
    plt.savefig(output_path, dpi=400)
    plt.show()


def main():
    # Define file paths (please adjust these paths as per your directory structure)
    shp_path = os.path.join(get_path_from_root("data", "raw", "shape_files_for_pa"), "PA_ZipCode_data.shp")
    demographic_path = os.path.join(get_path_from_root("data", "final"), "final_dp03.csv")
    gis_path = os.path.join(get_path_from_root("data", "interim"), "flattened_gis.csv")

    # Load shapefile, demographic data, and GIS data
    pa_shapefile = gpd.read_file(shp_path)
    demographic_data = pd.read_csv(demographic_path)
    gis_data = pd.read_csv(gis_path)

    chosen_factors = {
        "Employment Status - Population 16 years and over - In labor force - Civilian labor force - Employed":
            "EmpSta_Pop16&ovr_InLabFor_CivLabFor_Emp",
        "Income and benefits - Total households - Median household income (dollars)":
            "Inc&Ben_TotHou_MedHouInc",
        "Occupation - Civilian employed population 16 years and over - Service occupations":
            "Occ_CivEmpPop16ovr",
        "Industry - Civilian employed population 16 years and over - Arts, entertainment, and recreation, and accommodation and food services":
            "Ind_CivEmpPop16ovr_ArtEnt&Rec&Acc&FooSer",
        "Commuting to Work - Workers 16 years and over - Car, truck, or van -- drove alone":
            "Comm2Wor_Wor16ovr_CarTruVan_DriAlo",
        "Health Insurance Coverage - Civilian noninstitutionalized population - With health insurance coverage":
            "HeaInsCov_CivNonPop_WitHeaInsCov"
    }

    for keys, values in chosen_factors.items():
        create_chloropleth(gis_data, demographic_data, pa_shapefile, keys, values)


if __name__ == "__main__":
    main()
