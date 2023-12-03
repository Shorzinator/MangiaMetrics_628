import numpy as np
import pandas as pd
from scipy import stats

# Load the dataset
data = pd.read_csv(
    'C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\data\\interim\\demographic data\\DP04\\DP04_x_business_x_review.csv')

# Exclude non-numeric or identifier columns
exclude_features = ['ZIP Code', 'success_score']


# Function to categorize a numeric feature into quantiles
def categorize_feature(data, feature, n_quantiles=3):
    quantiles = data[feature].quantile(np.linspace(0, 1, n_quantiles + 1)).unique()  # Ensure unique quantiles
    categories = pd.cut(data[feature], bins=quantiles, labels=False, include_lowest=True)
    return categories


# Function to check homogeneity of variances using Levene's test
def check_homogeneity(data, feature, group_variable):
    grouped_data = [group.dropna() for name, group in data.groupby(group_variable)[feature]]

    # Ensure at least two non-empty groups are present
    if len(grouped_data) < 2 or any(group.empty for group in grouped_data):
        return {'Feature': feature, 'Levene_Stat': np.nan, 'Levene_P_Value': np.nan}

    stat, p_value = stats.levene(*grouped_data)
    return {'Feature': feature, 'Levene_Stat': stat, 'Levene_P_Value': p_value}


# Function to check normality assumption using Shapiro-Wilk test
def check_normality(data, feature):
    stat, p_value = stats.shapiro(
        data[feature].dropna().sample(min(50, len(data)), random_state=1))  # Sample due to test limitations
    return {'Feature': feature, 'Shapiro_Stat': stat, 'Shapiro_P_Value': p_value}


# Lists to collect assumption check results
homogeneity_results = []
normality_results = []

# Iterate over each feature to check assumptions, except 'success_score' and 'ZIP Code'
for feature in data.columns:
    if feature in exclude_features or not pd.api.types.is_numeric_dtype(data[feature]):
        continue  # Skip non-numeric features and excluded features

    # Categorize 'success_score' based on the current feature
    data['success_score_category'] = categorize_feature(data, 'success_score')

    # Check homogeneity of variances for the current feature, grouped by categorized 'success_score'
    homogeneity_results.append(check_homogeneity(data, feature, 'success_score_category'))

    # Check normality for the current feature
    normality_results.append(check_normality(data, feature))

# Convert results to DataFrames
homogeneity_df = pd.DataFrame(homogeneity_results)
normality_df = pd.DataFrame(normality_results)

# Save results to CSV
normality_df.to_csv(
    'C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\results\\eda\\Phase 2\\DP04_analysis\\normality_assumption_results.csv',
    index=False)
homogeneity_df.to_csv(
    'C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\results\\eda\\Phase 2\\DP04_analysis\\homogeneity_assumption_results.csv',
    index=False)

print("Assumption checks completed and results saved to CSV files.")
