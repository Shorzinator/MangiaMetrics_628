import os

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from pandas.plotting import parallel_coordinates
import matplotlib.pyplot as plt
import seaborn as sns

from scripts.utility.path_utils import get_path_from_root

# Load the data
# Assuming the file path is correct and data is in the same format as previously loaded
file_path = get_path_from_root("data", "interim", "demographic data", "DP04", "DP04_x_business_x_review.csv")
data = pd.read_csv(file_path)

# Select relevant features for clustering (including 'success_score' and key housing-related features)
features = ['success_score'] + [col for col in data.columns if 'Housing' in col]

# Extracting the relevant columns
clustering_data = data[features]

# Data Normalization
scaler = StandardScaler()
normalized_data = scaler.fit_transform(clustering_data)

# Perform K-Means clustering with 4 clusters
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(normalized_data)

# Add the cluster labels to the original data
data['Cluster'] = clusters

# Calculate the mean of the features for each cluster
cluster_means = data.groupby('Cluster')[features].mean()

# Normalize the cluster means for parallel plot
cluster_means_normalized = (cluster_means - cluster_means.min()) / (cluster_means.max() - cluster_means.min())

# Reset index to turn the clusters into a column
cluster_means_normalized = cluster_means_normalized.reset_index()

# Creating the parallel coordinates plot
plt.figure(figsize=(15, 10))
parallel_coordinates(cluster_means_normalized, 'Cluster', colormap='viridis', alpha=0.5)

# Enhancing the plot aesthetics
plt.title('Parallel Coordinates Plot for 4-Cluster Analysis', fontsize=16)
plt.xlabel('Features', fontsize=14)
plt.ylabel('Normalized Feature Values', fontsize=14)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Cluster', loc='center left', bbox_to_anchor=(1, 0.5))
plt.grid(True)

# Adjust the y-axis labels (not mandatory, just for aesthetics)
plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))

# Increase the bottom margin to prevent cutting off the x-axis labels
plt.gcf().subplots_adjust(bottom=0.3)

plt.savefig(os.path.join(get_path_from_root("results", "eda", "Phase 2", "DP04_analysis"), "cluster_analysis_parCoordPlot.png"))
plt.show()
