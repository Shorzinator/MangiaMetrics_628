import os

import pandas as pd
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from tqdm import tqdm

from scripts.utility.path_utils import get_path_from_root


def get_postcode(lat, lon):
    geolocator = Nominatim(user_agent="mangiaMetrics")
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True)
        if location:
            return location.raw.get('address', {}).get('postcode')
    except GeocoderTimedOut:
        return None


def main():
    # Load your dataset
    path = os.path.join(get_path_from_root("data", "interim"), "flattened_gis.csv")
    df = pd.read_csv(path)

    # Iterate over DataFrame rows and fill missing postcodes
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        if pd.isna(row['addr:postcode']) and pd.notna(row['latitude']) and pd.notna(row['longitude']):
            postcode = get_postcode(row['latitude'], row['longitude'])
            df.at[index, 'addr:postcode'] = postcode

    # Save the updated DataFrame
    df.to_csv("updated_flattened_gis.csv", index=False)


if __name__ == '__main__':
    main()
