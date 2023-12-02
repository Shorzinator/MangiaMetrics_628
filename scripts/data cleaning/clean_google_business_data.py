import json
import re
from datetime import datetime

import pandas as pd


def process_google_hours(hours_list):
    # Check if hours_list is a list and not null
    if hours_list and isinstance(hours_list, list):
        # Convert the list of lists into a dictionary
        hours_dict = {day_time[0]: day_time[1] for day_time in hours_list}
    else:
        # Return empty strings for each day if hours_list is null or not a list
        hours_dict = {}

    # Initialize a dictionary to hold the processed hours for each day
    processed_hours = {
        'hours_Monday': hours_dict.get('Monday', ''),
        'hours_Tuesday': hours_dict.get('Tuesday', ''),
        'hours_Wednesday': hours_dict.get('Wednesday', ''),
        'hours_Thursday': hours_dict.get('Thursday', ''),
        'hours_Friday': hours_dict.get('Friday', ''),
        'hours_Saturday': hours_dict.get('Saturday', ''),
        'hours_Sunday': hours_dict.get('Sunday', '')
    }

    return processed_hours


def extract_address_components(address):
    # Regular expression to extract address, city, state, and ZIP code
    # Assumes the format 'Business Name, Address, City, State ZIP'
    regex = r'[^,]+,\s*(?P<Address>[^,]+),\s*(?P<City>[^,]+),\s*(?P<State>[A-Z]{2})\s*(?P<ZIP>\d{5})'
    match = re.search(regex, address)

    if match:
        return match.groupdict()
    else:
        return {'address': '', 'city': '', 'state': '', 'ZIP Code': ''}


def convert_to_24hr(time_str):
    if time_str in ['Closed', '']:
        return time_str
    try:
        # Split the time range into start and end times
        start_time, end_time = time_str.split('–')

        # Check if AM/PM is missing in the start time
        if 'AM' not in start_time and 'PM' not in start_time:
            # If end time is PM and start time is less than 12, assume PM for start time
            if 'PM' in end_time and int(start_time.split(':')[0]) < 12:
                start_time += 'PM'
            else:
                start_time += 'AM'

        # Convert each time to 24-hour format
        start_time_24hr = datetime.strptime(start_time, '%I%p').strftime('%H:%M')
        end_time_24hr = datetime.strptime(end_time, '%I%p').strftime('%H:%M')

        return start_time_24hr + '–' + end_time_24hr
    except ValueError:
        return time_str  # Return original string if there's an error in conversion


def convert_hours_columns(df):
    hours_columns = [col for col in df.columns if col.startswith('hours_')]

    for col in hours_columns:
        df[col] = df[col].apply(convert_to_24hr)

    return df


def clean_google_business_data(file_path_google):
    # Load the Google Maps business.json file
    with open(file_path_google, 'r') as file:
        google_data = [json.loads(line) for line in file]

    # Convert to DataFrame
    google_df = pd.DataFrame(google_data)

    # Drop columns that are not needed
    google_df.drop(['description', 'price', 'MISC', 'relative_results', 'url'], axis=1, inplace=True)

    # Select and rename columns
    google_df = google_df.rename(columns={
        'avg_rating': 'stars',
        'num_of_reviews': 'review_count',
        'state': 'is_open'
    })

    # Apply the function to the 'hours' column in the Google data DataFrame
    google_df['hours'] = google_df['hours'].apply(process_google_hours)

    # Split the dictionary into separate columns
    hours_df = google_df['hours'].apply(pd.Series)
    google_df = pd.concat([google_df.drop(['hours'], axis=1), hours_df], axis=1)

    # Handle missing values
    google_df.dropna(subset=['category'], inplace=True)

    # Filter for Italian Restaurants
    google_df = google_df[google_df['category'].apply(lambda x: 'Italian Restaurant' in x
                                                                or 'Italian restaurant' in x
                                                                or 'italian restaurant' in x
                                                                or 'Italian' in x)]

    # Keep only open businesses
    google_df = google_df[google_df['is_open'].str.contains("open", case=False, na=False)]

    # Drop the 'is_open' column as it's no longer needed
    google_df.drop('is_open', axis=1, inplace=True)

    # Data type correction and alignment with Yelp data
    google_df['stars'] = pd.to_numeric(google_df['stars'], errors='coerce')
    google_df['review_count'] = pd.to_numeric(google_df['review_count'], errors='coerce')

    # Apply the function to split address into components
    address_components = google_df['address'].apply(extract_address_components)
    address_components_df = address_components.apply(pd.Series)

    # Concatenate the new address component columns with the main DataFrame
    google_df = pd.concat([google_df, address_components_df], axis=1)

    google_df = google_df.rename(columns={
        'Address': 'address',
        'State': 'state',
        'ZIP': 'ZIP Code',
        'City': 'city'
    })

    # Drop the original 'business_address' column as it's no longer needed
    google_df.drop(['address', 'category'], axis=1, inplace=True)

    google_df = convert_hours_columns(google_df)

    # Save the cleaned Google Maps data to CSV
    google_df.to_csv('C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\data\\interim\\cleaned_google_business.csv',
                     index=False)

    # return google_df


if __name__ == "__main__":
    file_path_google = 'C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\data\\raw\\Google Maps Data\\business_PA.json'
    clean_google_business_data(file_path_google)
