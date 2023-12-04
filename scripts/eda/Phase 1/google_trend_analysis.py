import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from scipy.stats import linregress
import numpy as np

data = pd.read_csv('C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\data\\raw\\Google Trend Data\\InterestOverTime_since2018.csv')

# Convert the 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Convert 'Date' to a numerical format for regression analysis
data['DateNum'] = mdates.date2num(data['Date'])

# Perform linear regression
slope, intercept, r_value, p_value, std_err = linregress(data['DateNum'], data['Italian_Restaurant_in_PA'])

# Create a scatter plot with improved style
plt.figure(figsize=(12, 7))
plt.scatter(data['Date'], data['Italian_Restaurant_in_PA'], color='blue', s=50, alpha=0.6, label='Search Interest')

# Add the regression line with annotation
reg_line = intercept + slope * data['DateNum']
plt.plot(data['Date'], reg_line, color='darkorange', label=f'Regression Line (slope: {slope:.2f}, intercept: {intercept:.2f})')

# Calculate and annotate the R-squared value
plt.text(data['Date'].iloc[-20], max(data['Italian_Restaurant_in_PA']), f'$R^2$: {r_value**2:.2f}', fontsize=12, color='darkorange')

# Improve the readability of the x-axis
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gcf().autofmt_xdate()  # Rotation

# Set the title and labels with improved fonts
plt.title('Trend of Italian Food Interest in Pennsylvania (2018-2023)', fontsize=16, fontweight='bold')
plt.xlabel('Year', fontsize=14, fontweight='bold')
plt.ylabel('Relative Search Interest', fontsize=14, fontweight='bold')

# Show legend
plt.legend()

# Show plot with a tight layout
plt.tight_layout()
plt.savefig("C:\\Users\\shour\\PycharmProjects\\MangiaMetrics_628\\results\\eda\\Phase 1\\Relative_Search_Interest_since_2018.png")
plt.show()
