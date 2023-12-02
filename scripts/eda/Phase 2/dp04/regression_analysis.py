import os

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from scripts.utility.path_utils import get_path_from_root

# Load the merged data for regression analysis
path = os.path.join(get_path_from_root("data", "interim", "demographic data", "DP04"),
                    "DP04_x_business_x_review.csv")
merged_data = pd.read_csv(path)

# Selecting only numeric columns for regression analysis
numeric_data = merged_data.select_dtypes(include=['float64', 'int64'])

# Define the dependent variable 'success_score' and independent variables (all other numeric columns)
X = numeric_data.drop(columns=['success_score'])  # Independent variables
y = numeric_data['success_score']  # Dependent variable

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
model = LinearRegression()

# Fit the model on the training data
model.fit(X_train, y_train)

# Predict success scores on the testing data
y_pred = model.predict(X_test)

# Calculate the model performance metrics
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

# Coefficients and Intercept
coefficients = model.coef_
intercept = model.intercept_

# Prepare a DataFrame to show coefficients for each feature
feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': coefficients
}).sort_values(by='Coefficient', ascending=False)

feature_importance.to_csv(os.path.join(get_path_from_root("results", "eda", "Phase 2", "DP04_analysis"),
                                       "regression_coefficient.csv"), index=False)

# Show the performance metrics and the feature importance
# print(r2, mse, intercept, feature_importance.head())  # Showing top 10 features for brevity
