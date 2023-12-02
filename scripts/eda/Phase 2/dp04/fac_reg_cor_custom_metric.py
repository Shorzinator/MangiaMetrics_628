import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


def create_custom_metric(dataframe):
    # Selecting the relevant columns for standardization
    relevant_columns = ['Coefficient', 'success_score']
    data_to_standardize = dataframe[relevant_columns]

    # Standardizing the data
    scaler = StandardScaler()
    standardized_data = scaler.fit_transform(data_to_standardize)

    # Creating the custom metric as the mean of the standardized values
    dataframe['custom_metric'] = np.mean(standardized_data, axis=1)

    # Selecting only the 'Feature' and 'custom_metric' columns for the output
    output_dataframe = dataframe[['Feature', 'custom_metric']]

    return output_dataframe


def main():
    data = (
        pd.read_csv(
            "C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\results\\eda\\Phase 2\\DP04_analysis\\merged_reg_fac_cor_analysis.csv"
        )
    )
    # Applying the function to the dataset
    custom_metric_df = create_custom_metric(data)

    # Saving the result to a CSV file
    output_file_path = "C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\results\\eda\\Phase 2\\DP04_analysis\\fac_reg_cor_custom_score.csv"
    custom_metric_df.to_csv(output_file_path, index=False)


if __name__ == "__main__":
    main()
