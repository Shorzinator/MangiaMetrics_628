import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from scripts.utility.path_utils import get_path_from_root

# Load the datasets
path = os.path.join(get_path_from_root("data", "interim", "demographic data", "DP04"),
                    "DP04_x_business_x_review.csv")

merged_data = pd.read_csv(path)

# Calculate the correlation matrix
correlation_matrix = merged_data.corr()

# Plot a heatmap of the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.savefig(os.path.join(get_path_from_root("results", "eda", "Phase 2", "DP04_analysis"), "correlation_heatmap.png"))
# plt.show()

# Print out the correlation of each feature with the success score
success_correlation = correlation_matrix['success_score'].sort_values(ascending=False)
success_correlation.to_csv(os.path.join(get_path_from_root("results", "eda", "Phase 2", "DP04_analysis"),
                                        "correlation_heatmap.csv"))
# print(success_correlation)
