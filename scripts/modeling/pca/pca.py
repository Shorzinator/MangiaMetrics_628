import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import seaborn as sns

from scripts.utility.path_utils import get_path_from_root

# Re-loading the datasets
dp03_df = pd.read_csv(get_path_from_root("data", "final", "final_dp03.csv"))
dp04_df = pd.read_csv(get_path_from_root("data", "final", "final_dp04.csv"))
dp05_df = pd.read_csv(get_path_from_root("data", "final", "final_dp05.csv"))

# Merging the datasets based on ZIP Code
merged_df = dp03_df.merge(dp04_df, on='ZIP_CODE', how='inner').merge(dp05_df, on='ZIP_CODE', how='inner')

# Selecting only numerical columns for PCA
numerical_cols = merged_df.select_dtypes(include=['float64', 'int64']).columns

# Preprocessing the data
# 1. Imputing missing values: Filling missing values with the mean of each column
# 2. Normalizing the data: Standardizing the features so that they are centered around 0 with a standard deviation of 1
imputer = SimpleImputer(strategy='mean')
merged_df[numerical_cols] = imputer.fit_transform(merged_df[numerical_cols])

scaler = StandardScaler()
merged_df_scaled = scaler.fit_transform(merged_df[numerical_cols])

# Performing PCA
pca = PCA()
pca.fit(merged_df_scaled)

# Cumulative explained variance ratio to determine how many components to keep
cumulative_explained_variance = pca.explained_variance_ratio_.cumsum()

# Find the number of components for 95% explained variance
num_components_95 = np.where(cumulative_explained_variance > 0.95)[0][0] + 1

# Plotting the cumulative explained variance against the number of components
plt.figure(figsize=(10, 6))
plt.plot(np.arange(1, len(cumulative_explained_variance) + 1), cumulative_explained_variance, marker='o')
plt.title('Cumulative Explained Variance by PCA Components')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.axhline(y=0.95, color='r', linestyle='--', label='95% Explained Variance')
plt.axhline(y=0.90, color='g', linestyle='--', label='90% Explained Variance')

# Add a vertical line at the point of 95% explained variance
plt.axvline(x=num_components_95, color='b', linestyle='--', label=f'95% variance at {num_components_95} components')

# Annotate the intersection point on the x-axis
ymin, ymax = plt.ylim()  # get the current y-axis limits
plt.annotate(str(num_components_95), (num_components_95, ymin), textcoords="offset points", xytext=(0,-20), ha='center', color='b')

plt.legend()
plt.grid(True)
plt.savefig(os.path.join(get_path_from_root("results", "modeling", "pca"), "CumExpVar_byPCA.png"))
# plt.show()

# Get the PCA components (loadings)
pca_components = pca.components_

# Create a DataFrame with the PCA components and feature names
pca_loadings_df = pd.DataFrame(pca_components, columns=numerical_cols, index=[f'PC{i}' for i in range(len(pca_components))])

# Identifying top features for each principal component based on loadings
top_features_by_pc = {}
for i, pc in enumerate(pca_loadings_df.index):
    loadings = pca_loadings_df.loc[pc].abs().sort_values(ascending=False)
    top_features = loadings.head(10).index.tolist()
    top_features_by_pc[pc] = top_features


# Visualizing top features for the first principal component
plt.figure(figsize=(10, 8))
sns.barplot(y=top_features_by_pc['PC0'], x=pca_loadings_df.loc['PC0', top_features_by_pc['PC0']])
plt.title('Top Feature Contributions to PC1')
plt.xlabel('Feature Contributions')
plt.ylabel('Features')
plt.savefig(os.path.join(get_path_from_root("results", "modeling", "pca"), "Top_Features.png"))
plt.show()

pca_loadings_df.to_csv(os.path.join(get_path_from_root("results", "modeling", "pca"), "pca_loadings.csv"))

# Output the top features for the first few principal components
# for pc, features in top_features_by_pc.items():
#     print(f"{pc} top contributing features: {features}")
