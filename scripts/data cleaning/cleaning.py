from scripts.utility.data_loader import get_business_df


def clean_business():
    business_df = get_business_df()

    # Filter for restaurants in Pennsylvania
    business_df = business_df[business_df['categories'].str.contains('Restaurants', na=False)]
    business_df = business_df[business_df['state'] == 'PA']

    # Remove businesses that are closed
    business_df = business_df[business_df["is_open"] == 1]

    # Remove duplicate entries based on business_id
    business_df = business_df.drop_duplicates(subset="business_id")

    # Normalize text in categories
