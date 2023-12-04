import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load the datasets
final_dp03 = pd.read_csv('C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\data\\final\\final_dp03.csv')
final_dp04 = pd.read_csv('C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\data\\final\\final_dp04.csv')
final_dp05 = pd.read_csv('C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\data\\final\\final_dp05.csv')
top_features = pd.read_csv('C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\results\\modeling\\pca\\top_features_merged.csv')

# Merging the datasets on 'ZIP_CODE'
merged_data = pd.merge(final_dp03, final_dp04, on='ZIP_CODE', how='outer')
merged_data = pd.merge(merged_data, final_dp05, on='ZIP_CODE', how='outer')

# Extracting the feature names from the 'top_features' dataset
top_feature_names = top_features['Feature'].tolist()

# Selecting these features from the merged dataset
# Adding 'ZIP_CODE' to the list as it's our key column
selected_features = ['ZIP_CODE'] + [feature for feature in top_feature_names if feature in merged_data.columns]

# Creating a new dataset with only the top features
top_features_data = merged_data[selected_features]

# Normalizing the data (excluding the ZIP_CODE column)
scaler = MinMaxScaler()
normalized_data = scaler.fit_transform(top_features_data.iloc[:, 1:])

# Assigning equal weights to all features
num_features = normalized_data.shape[1]
weights = [1 / num_features] * num_features

# Calculating the composite metric
composite_metric = normalized_data.dot(weights)

# Creating a new dataframe with ZIP code and composite metric
composite_metric_df = pd.DataFrame({
    'ZIP_CODE': top_features_data['ZIP_CODE'],
    'Composite_Metric': composite_metric
})

# Rescaling the composite metric to a range of 0 to 100
composite_metric_df['Composite_Metric'] = composite_metric_df['Composite_Metric'] * 100

# Save the final dataframe to a CSV file
composite_metric_df.to_csv('C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\data\\interim\\composite_metric.csv',
                           index=False)
