import os

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import FactorAnalysis
from sklearn.preprocessing import StandardScaler

from scripts.utility.path_utils import get_path_from_root

# Load the data, assuming you have enough memory to do this step
path = os.path.join(get_path_from_root("data", "interim", "demographic data", "DP04"),
                    "DP04_x_business_x_review.csv")
data = pd.read_csv(path)

# Select only numeric columns for factor analysis and exclude 'success_score'
numeric_data = data.select_dtypes(include=['float64', 'int64']).drop(columns=['success_score'])

# Standardize the features before performing factor analysis
scaler = StandardScaler()
X_scaled = scaler.fit_transform(numeric_data)

# Initialize the Factor Analysis object with the number of components you wish to extract
fa = FactorAnalysis(n_components=5, random_state=42)

# Fit the model to the standardized data
fa.fit(X_scaled)

# Check the loadings of each variable on the factors
loadings = pd.DataFrame(fa.components_.T, columns=['Factor {}'.format(i + 1) for i in range(fa.n_components)],
                        index=numeric_data.columns)

loadings.to_csv(os.path.join(get_path_from_root("results", "eda", "Phase 2", "DP04_analysis"),
                             "factor_loadings.csv"))

# Plot the loadings for the first couple of factors, for example
plt.figure(figsize=(50, 50))
loadings[['Factor 1', 'Factor 2', 'Factor 3', 'Factor 4', 'Factor 5']].head(3).plot(kind='bar')
plt.title('Factor Loadings')
plt.xticks(rotation=45, ha="right")
# plt.savefig("factor loadings")
# plt.show()
