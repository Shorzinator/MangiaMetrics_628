import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import KNNImputer
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from scripts.utility.path_utils import get_path_from_root


# Function to preprocess data
def preprocess_data(df, target):
    X = df.drop(target, axis=1)
    y = df[target]
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns

    # Use SparseThreshold to control the sparsity/density of the output
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ],
        remainder='passthrough',
        sparse_threshold=0
    )
    return X, y, preprocessor


# Function to build and fit the model
def build_and_fit_model(X, y, preprocessor):
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('imputer', KNNImputer(n_neighbors=5)),
        ('regressor', RandomForestRegressor(random_state=42))
    ])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f'Mean Squared Error: {mse}')
    return model, X_train, y_train, X_test, y_test


# Function to plot and save feature importances
def plot_and_save_importances(model, X, preprocessor, file_name, output_path):
    # Retrieve feature names after transformation
    feature_names = preprocessor.transformers_[0][1].get_feature_names_out().tolist()
    feature_names += X.columns[len(preprocessor.transformers_[0][2]):].tolist()

    # Get importances from the model
    importances = model.named_steps['regressor'].feature_importances_
    indices = np.argsort(importances)[::-1]

    # Ensure the number of feature names matches the number of importances
    if len(feature_names) != len(importances):
        print("Mismatch in the number of features and importances")
        return

    # Plot Feature Importances
    # plt.figure()
    # plt.title("Feature importances")
    # plt.bar(range(len(importances)), importances[indices], align="center")
    # plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation='vertical')
    # plt.xlim([-1, len(importances)])
    # plt.tight_layout()
    # plt.savefig(os.path.join(output_path, f'{file_name}_feature_importance.png'))

    # Save Feature Importances to CSV
    feature_importances = pd.DataFrame(
        {
            'Feature': [feature_names[i] for i in indices],
            'Importance': importances[indices]}
    )

    feature_importances.to_csv(os.path.join(output_path, f'{file_name}_feature_importance.csv'), index=False)


# Main execution function
def main():
    df_path = get_path_from_root("data", "interim", "demographic data", "DP03", "DP03_x_business_x_review.csv")
    df = pd.read_csv(df_path)
    output_path = get_path_from_root("results", "modeling", "DP03")

    X, y, preprocessor = preprocess_data(df, 'success_score')
    model, X_train, y_train, X_test, y_test = build_and_fit_model(X, y, preprocessor)

    plot_and_save_importances(model, X_train, preprocessor, 'random_forest', output_path)


if __name__ == "__main__":
    main()
