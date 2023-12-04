import os

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

from scripts.utility.path_utils import get_path_from_root

# Load your datasets
dp03_df = pd.read_csv(get_path_from_root("data", "interim", "demographic data", "DP03", "DP03_x_business_x_review.csv"))
dp04_df = pd.read_csv(get_path_from_root("data", "interim", "demographic data", "DP04", "DP04_x_business_x_review.csv"))
dp05_df = pd.read_csv(get_path_from_root("data", "interim", "demographic data", "DP05", "DP05_x_business_x_review.csv"))

# Merge the datasets based on ZIP Code
merged_df = dp03_df.merge(dp04_df, on='ZIP Code', how='inner').merge(dp05_df, on='ZIP Code', how='inner')

# Keep only numerical columns
numerical_cols = merged_df.select_dtypes(include=['float64', 'int64']).columns
merged_numerical_df = merged_df[numerical_cols]

# Impute missing values and standardize the data
imputer = SimpleImputer(strategy='mean')
merged_imputed_df = pd.DataFrame(imputer.fit_transform(merged_numerical_df), columns=merged_numerical_df.columns)
scaler = StandardScaler()
merged_scaled_df = pd.DataFrame(scaler.fit_transform(merged_imputed_df), columns=merged_imputed_df.columns)

# Perform PCA
pca = PCA()
pca.fit(merged_scaled_df)

# Cumulative explained variance ratio to determine how many components to keep
cumulative_explained_variance = pca.explained_variance_ratio_.cumsum()

# Find the number of components for 90% and 95% explained variance
num_components_90 = np.where(cumulative_explained_variance > 0.90)[0][0] + 1
num_components_95 = np.where(cumulative_explained_variance > 0.95)[0][0] + 1

# Plotting the cumulative explained variance against the number of components
plt.figure(figsize=(10, 6))
plt.plot(np.arange(1, len(cumulative_explained_variance) + 1), cumulative_explained_variance, marker='o')
plt.title('Cumulative Explained Variance by PCA Components')
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.axhline(y=0.95, color='r', linestyle='--', label='95% Explained Variance')
plt.axhline(y=0.90, color='g', linestyle='--', label='90% Explained Variance')
plt.axvline(x=num_components_95, color='b', linestyle='--', label=f'95% variance at {num_components_95} components')
plt.axvline(x=num_components_90, color='purple', linestyle='--', label=f'90% variance at {num_components_90} components')
plt.legend()
plt.grid(True)
plt.savefig(os.path.join(get_path_from_root("results", "modeling", "pca"), "CumExpVar_byPCA.png"))
plt.show()

# Get the PCA components (loadings)
pca_loadings = pd.DataFrame(pca.components_, columns=merged_scaled_df.columns, index=[f'PC{i+1}' for i in range(len(pca.components_))])
# Save the PCA loadings
# pca_loadings.to_csv(os.path.join(get_path_from_root("results", "modeling", "pca"), "pca_loadings.csv"))

# Transpose the PCA loadings DataFrame so that principal components become columns
pca_loadings_transposed = pca_loadings.transpose()

# Visualizing top features for the first principal component (PC1)
top_features_pc1 = pca_loadings_transposed['PC1'].abs().nlargest(10).index.tolist()
sns.barplot(y=top_features_pc1, x=pca_loadings_transposed.loc[top_features_pc1, 'PC1'])
plt.title('Top Feature Contributions to PC1')
plt.xlabel('Feature Contributions')
plt.ylabel('Features')
plt.show()
