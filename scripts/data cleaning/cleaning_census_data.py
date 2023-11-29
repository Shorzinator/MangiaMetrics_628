import os

import pandas as pd

from scripts.utility.path_utils import get_path_from_root


def clean_census_data(input_path, output_path):
    input_path = input_path
    output_path = output_path

    # Read the CSV file
    df = pd.read_csv(input_path)

    # Process initial hierarchical structure
    def count_leading_spaces(value):
        if isinstance(value, str):
            return len(value) - len(value.lstrip(' '))
        else:
            return 0

    df['IndentLevel'] = df['Label (Grouping)'].apply(count_leading_spaces)

    max_indent = df['IndentLevel'].max()
    for level in range(max_indent + 1):
        df[f'Level_{level}'] = None
        mask = df['IndentLevel'] == level
        df.loc[mask, f'Level_{level}'] = df.loc[mask, 'Label (Grouping)'].str.strip()

    for level in range(max_indent + 1):
        df[f'Level_{level}'] = df[f'Level_{level}'].ffill()

    df.drop(columns=['Label (Grouping)'], inplace=True)

    # Update 'Level_0' to represent the hierarchy
    def update_hierarchy_column(df):
        current_path = []  # Initialize an empty list to store the current hierarchy path
        hierarchy = []  # Initialize an empty list to store the final hierarchy for each row

        for index, row in df.iterrows():
            label = row['Level_0']
            indent_level = row['IndentLevel']

            # Truncate the current_path list to the current indent_level
            current_path = current_path[:indent_level]

            if indent_level == 0 and label.isupper():  # Major category
                current_path = [label]  # Start a new path
            elif label.endswith(':'):  # Subcategory
                if len(current_path) > indent_level:
                    current_path[indent_level] = label  # Replace at the current indent level
                else:
                    current_path.append(label)  # Append to the current path
            else:  # Continuation of the current hierarchy
                if len(current_path) > indent_level:
                    current_path[indent_level] = label  # Replace at the current indent level
                else:
                    current_path.append(label)  # Append if empty or extend the path

            hierarchy.append(' -> '.join(current_path))

        df['Level_0'] = hierarchy
        return df

    df = update_hierarchy_column(df)

    # Standardize ZIP code column names
    def standardize_zip_code_columns(df):
        for col in df.columns:
            if 'ZCTA5' in col and '!!Estimate' in col:
                new_col_name = col.split()[1]  # Extracting the ZIP code
                df.rename(columns={col: new_col_name}, inplace=True)

        df.columns = [col.replace("!!Estimate", "") for col in df.columns]
        return df

    df = standardize_zip_code_columns(df)

    # Drop redundant columns
    columns_to_drop = [col for col in df.columns if 'Margin of Error' in col or 'Percent' in col]
    df.drop(columns=columns_to_drop, inplace=True)

    # Save the cleaned DataFrame
    df.to_csv(output_path, index=False)


def main():
    input_paths = {
        "DP04": os.path.join(get_path_from_root("data", "raw", "Census Bureau Data"), "DP04.csv"),
        "DP05": os.path.join(get_path_from_root("Data", "raw", "Census Bureau Data"), "DP05.csv")
    }

    output_paths = {
        "DP04": os.path.join(get_path_from_root("data", "interim"), "cleaned_dp04.csv"),
        "DP05": os.path.join(get_path_from_root("Data", "interim"), "cleaned_dp05.csv")
    }

    for key in input_paths.keys():
        clean_census_data(input_paths[key], output_paths[key])


if __name__ == "__main__":
    main()
