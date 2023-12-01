import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from scripts.utility.data_loader import get_clean_business_df, get_business_df

# Call the function to load the data
# df = get_business_df()


# Function to safely evaluate a string representation of a dictionary
def safe_eval_dict(d):
    try:
        return eval(d)
    except:
        return {}


# Check if the DataFrame needs normalization
if any(df.map(lambda x: isinstance(x, dict)).any()):
    # Normalize the 'attributes' and 'hours' columns
    attributes_df = pd.json_normalize(df['attributes'].dropna().tolist()).add_prefix('attributes_')
    hours_df = pd.json_normalize(df['hours'].dropna().tolist()).add_prefix('hours_')

    # Further normalize specific keys within 'attributes'
    for key in ['GoodForMeal', 'BusinessParking', 'Ambience']:
        # Extract and normalize the nested dictionaries
        nested_df = pd.json_normalize(attributes_df[f'attributes_{key}'].dropna().apply(safe_eval_dict)).add_prefix(
            f'{key}_')
        # Drop the original column from attributes_df
        attributes_df = attributes_df.drop(columns=[f'attributes_{key}'])
        # Merge the normalized dataframes back into the attributes_df
        attributes_df = attributes_df.join(nested_df, how='left')

    # Drop the original 'attributes' and 'hours' columns from df
    df = df.drop(columns=['attributes', 'hours'])

    # Merge the normalized dataframes back into the original dataframe
    df = df.join(attributes_df, how='left').join(hours_df, how='left')

    # Remove 'attributes_' prefix from column names
    df.columns = [col.replace('attributes_', '') for col in df.columns]

    df.to_csv("unclean_flattened_business.csv", index=False)

# print(df.columns)
# print(df.head(10))