import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np

# Load the dataset
dp04_df = pd.read_csv('C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\data\\final\\final_dp04.csv')

# Define columns for housing units built and household movement
structure_built_cols = [
    'Year structure built - Total housing units - Built 2000 to 2009',
    'Year structure built - Total housing units - Built 2010 to 2019',
    'Year structure built - Total housing units - Built 2020 or later'
]

householder_move_in_cols = [
    'Year householder move into unit - Occupied housing units - Moved in 2019 or later',
    'Year householder move into unit - Occupied housing units - Moved in 2015 to 2018',
    'Year householder move into unit - Occupied housing units - Moved in 2010 to 2014',
    'Year householder move into unit - Occupied housing units - Moved in 2000 to 2009'
]

# Extract relevant data and convert to numeric
dp04_analysis_df = dp04_df[structure_built_cols + householder_move_in_cols]
dp04_analysis_df = dp04_analysis_df.apply(pd.to_numeric, errors='coerce').fillna(0)

# Aggregate data
structure_built_totals = dp04_analysis_df[structure_built_cols].sum()
householder_move_in_totals = dp04_analysis_df[householder_move_in_cols].sum()

# Preparing data for smoothing
# For smoothing, we need numeric representations of years
year_numeric = np.array([0, 1, 2, 3])  # Representing 2000-2009, 2010-2014, 2015-2018, 2019-Later

# Creating spline functions for smooth curves
spl_structure_built = make_interp_spline(year_numeric[:3], structure_built_totals.values, k=2)  # Only 3 data points for structure built
spl_householder_move_in = make_interp_spline(year_numeric, householder_move_in_totals.values, k=2)

# Generating smooth data points
xnew = np.linspace(year_numeric.min(), year_numeric.max(), 300)
smooth_structure_built = spl_structure_built(xnew[:200])  # Only 3 data points for structure built
smooth_householder_move_in = spl_householder_move_in(xnew)

# Creating a more intuitive year labeling
years_label = ['2000-2009', '2010-2014', '2015-2018', '2019-Later']

# Re-plotting with smooth lines and improved aesthetics
plt.figure(figsize=(12, 6))
plt.plot(xnew[:200], smooth_structure_built, label='Housing Units Built', color='royalblue', linewidth=2)
plt.plot(xnew, smooth_householder_move_in, label='Residents Moved In', color='seagreen', linewidth=2)

# Adding scatter points for actual data
plt.scatter(year_numeric[:3], structure_built_totals, color='royalblue')
plt.scatter(year_numeric, householder_move_in_totals, color='seagreen')

# Improving labels and title
plt.title('Trends in Housing Development and Household Movement (2000-2022)', fontsize=16)
plt.xlabel('Time Period', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.xticks(ticks=year_numeric, labels=years_label, fontsize=12)
plt.yticks(fontsize=12)

plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.savefig("C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\results\\eda\\Phase 2\\DP04_analysis\\trends_housing_development_and_movement.png")
print("saved")
# Show the plot
plt.show()
