# Tests to be done on all demographic datasets -

To systematically analyze the factors that may contribute to the success of Italian restaurants and identify potential
locations for new ventures, you can follow a stepwise approach using the following tests, in order of complexity and
depth of insights they provide:

## 1. Correlation Analysis:

Start with this to quickly identify any linear relationships between individual factors (
like median income, population density) and restaurant success indicators (like average restaurant revenue in the
area). A high positive correlation coefficient would suggest that as one variable increases, so does the other. For
example, if median income has a high positive correlation with restaurant success, it indicates areas with higher
income might support more expensive dining options.
After performing correlation analysis, we can use the factors most correlated with the success metric we have
calculated, we will choose those and make a chloropleth to support our quantitative findings.

### 1. Results from DP04 -

1. Positive Correlations:
    1. High Occupancy Density: Factors like 'Occupants per room - Occupied housing units - 1.51 or more' and 'GRAPI -
       Occupied units paying rent - 15.0 to 19.9 percent' have positive correlations. This suggests that areas with
       higher
       occupancy rates, possibly indicating higher population density, correlate with higher success scores for
       restaurants.
    2. Older Structures: 'Year structure built - Total housing units - Built 1939 or earlier' has a relatively high
       positive
       correlation, implying that neighborhoods with older buildings might have established communities and stable
       customer
       bases.

    3. Smaller Living Spaces: Factors such as 'Rooms - Total housing units - 2 rooms' and 'Rooms - Total housing units -
       3
       rooms' have positive correlations. This could indicate that areas with smaller living spaces, which might include
       urban
       centers or areas with higher population density, have successful restaurants due to higher foot traffic and a
       potentially larger customer base.

    4. Higher Rent Burden: GRAPI (Gross Rent as a Percentage of Household Income) indicators show positive correlations
       in
       several brackets, suggesting that areas where a higher proportion of income is spent on rent might still have
       successful
       restaurants, possibly due to the lack of home cooking or the cultural value of dining out.

2. Negative Correlations:

    1. Vehicle Availability: 'Vehicles available - Occupied housing units - 3 or more vehicles available' has a strong
       negative
       correlation. This could imply that areas where residents rely less on public transport and more on personal
       vehicles may
       not be as successful for restaurants, perhaps due to the suburban setting and the propensity for home cooking or
       dining
       options outside the immediate neighborhood.

    2. Detached Single-Family Homes: 'Units in Structure - Total housing units - 1-unit, detached' negatively correlates
       with
       success score, which suggests that areas with a prevalence of single-family homes may not be the best locations
       for
       Italian restaurants, potentially due to lower walkability and a different lifestyle.

    3. Higher Home Values: Factors related to the value of owner-occupied units, particularly at higher price points,
       show
       negative correlations. This could indicate that wealthier neighborhoods may not necessarily translate into more
       successful restaurant ventures, possibly due to different dining preferences or the availability of diverse
       dining
       options.

    4. Larger Homes: The negative correlation with 'Rooms - Total housing units - 9 rooms or more' and 'Bedrooms - Total
       housing units - 5 or more bedrooms' suggests that neighborhoods with larger homes, which may reflect
       family-oriented and
       possibly more affluent areas, do not correlate as strongly with restaurant success.

3. Combined Analysis:
    1. The data suggests that Italian restaurants in Pennsylvania tend to be more successful in densely populated areas
       with a
       high occupancy rate, where residents may be younger or more transient, such as in urban centers or neighborhoods
       with
       older, smaller housing units. These areas might offer a steady flow of customers who value convenience and social
       dining
       experiences.

    2. On the contrary, areas characterized by larger homes, higher vehicle dependency, and potentially suburban
       settings might be less ideal for new Italian restaurants due to factors like lower foot traffic, a stronger
       likelihood of dining at home, and possibly a preference for different types of dining experiences.

    3. In conclusion, when considering locations for new Italian restaurants or assessing the factors contributing to
       the
       success of existing ones, a focus on population density, housing type, and the age of the neighborhood could
       provide
       valuable insights. Areas with smaller, older residences and higher rental burdens appear to be more favorable,
       possibly
       due to lifestyle and dining habits conducive to frequenting restaurants.

## 2. Regression Analysis:

After identifying correlated factors, regression can help model the relationship between
multiple independent variables (demographic factors) and a dependent variable (restaurant success). Multiple
regression can show not only which factors have a statistically significant relationship with restaurant success but
also the strength of these relationships. For instance, it might reveal that while both median income and population
density are related to success, median income is a much stronger predictor.

### 1. Results from DP03 -

### 2. Results from DP04 -

1. The R-squared value is approximately 0.090, which indicates that about 9% of the variability in the success
   score can be explained by the model with the given demographic factors. This suggests that while there is some
   relationship between these factors and restaurant success, a large portion of the variability is still unexplained by
   the model.

2. The mean squared error (MSE) is approximately 0.353,
   which provides an average of the squares of the errors—that is,
   the average squared difference between the estimated values and the actual value of the success score.
   The regression coefficients indicate the expected change in the success score associated with a one-unit change in
   the predictor variable, holding other variables constant.
   The model's intercept is approximately 1.62, which can be
   interpreted as the expected success score when all the predictor variables are zero.

3. The top factors with the highest positive coefficients are as follows:

    1. Occupied Housing Units: A strong positive coefficient suggests that a higher number of occupied housing units is
       associated with higher success scores.

    2. Gross Rent - Occupied Units Paying Rent: Indicates that higher gross rents paid by occupied units are associated
       with
       higher success scores.

    3. Housing Tenure: The status of housing tenure has a significant positive relationship with the success score.

    4. Vehicles Available: The availability of vehicles in occupied housing units shows a strong positive association
       with the
       success score.

    5. House Heating Fuel: The type of heating fuel used in occupied housing units seems to have a significant positive
       impact.

These coefficients provide insights into how demographic factors might influence the success of restaurants. However,
the relatively low R-squared value suggests that other unconsidered factors may also play a significant role in
restaurant success. These could include factors such as restaurant quality, management, competition, accessibility, and
local food preferences.

### 3. Results from DP05

## 3. Factor Analysis:

This is useful if there are many interrelated variables and you want to identify underlying
dimensions. Factor analysis can reduce the number of variables by grouping them into factors based on their
correlations. For instance, if various income-related variables all correlate with each other and with restaurant
success, factor analysis might combine them into a single "economic" factor for further analysis.

### 1. Results from DP03 -

### 2. Results from DP04 -

### Insights

1. **Factor 1 Loadings**: High loadings on features related to housing occupancy and units in structure. This suggests
   that Factor 1 might be capturing aspects related to residential density or types of housing. For instance, 'Housing
   Occupancy - Total housing units' has a very high loading, indicating its strong relation with this factor.

2. **Factor 2 Loadings**: Notable for its contrast in loadings, such as positive loading for 'Housing Occupancy - Total
   housing units - Vacant units' and negative for 'Units in Structure - Total housing units - 1-unit, attached'. This
   factor may be reflecting differences in housing styles or occupancy rates, perhaps distinguishing urban from suburban
   or rural areas.

3. **Factors 3, 4, and 5 Loadings**: These factors show smaller loadings for the top features, suggesting they might be
   capturing more nuanced or specific aspects of the data, possibly related to smaller segments of the population or
   less dominant housing trends.

### Alignment with Project Aim

Our project aims to identify potential locations for Italian restaurants in Pennsylvania by analyzing demographic
trends, consumer preferences, and transportation accessibility.
Here's how the factor analysis aligns with this aim:

1. **Demographic Trends**: Factors 1 and 2, with their focus on housing occupancy and structure, can inform you about
   population density and housing styles in different areas. These trends are crucial for understanding where potential
   customers for Italian restaurants live and how their living arrangements might influence dining preferences.

2. **Consumer Preferences**: The variation in housing types and occupancy can be indicative of different lifestyles and,
   by extension, dining preferences. For instance, areas with high-density housing might favor quick-service or takeaway
   options, while areas with single-family homes might prefer dine-in experiences.

3. **Location Selection for New Ventures**: By understanding which factors strongly correlate with successful Italian
   restaurants, you can prioritize locations that exhibit these characteristics. For example, if Factor 1 (linked to
   residential density) is a strong predictor of success, focusing on densely populated areas might be beneficial.

4. **Expansion of Existing Restaurants**: Insights from these factors can guide existing Italian restaurants in
   tailoring their services or marketing strategies to align with the demographic and lifestyle characteristics of their
   area.

#### Specific Recommendations

To leverage these insights effectively:

- **Focus on Areas with High Factor 1 and 2 Scores**: These are likely to represent regions with favorable demographic
  and housing characteristics for Italian restaurants.
- **Consider Nuanced Insights from Factors 3, 4, and 5**: Although these factors have smaller loadings, they might
  capture specific trends or niches that could be relevant for targeted marketing or specialized Italian restaurant
  concepts.
- **Cross-reference with Other Data**: Integrate these findings with other analyses like regression and correlation to
  build a comprehensive understanding of the factors influencing the success of Italian restaurants.

Remember, factor analysis offers a broad view of underlying trends and should be complemented with detailed local market
research to make informed business decisions.

### Results from DP05 -

## Cluster Analysis:

This method can classify zip codes into clusters based on similarity in the factors identified
as important. This will help in identifying not just individual locations but also regions where new Italian
restaurants are more likely to succeed. For example, if several zip codes have similar income levels, demographics,
and lack of Italian restaurants, they might form a cluster representing a high potential for new ventures.

### Results from DP03 - 

### Results from DP04 - 
### Cluster 3

- **Success Score**: Highest average success score (approximately 2.05), suggesting that ZIP codes in this cluster have
  the most successful Italian restaurants.
- **Housing Units**: Moderate number of total housing units, with a high percentage of those units being occupied, which
  may indicate a stable and potentially lucrative customer base.
- **Vacancy Rates**: Slightly higher homeowner vacancy rates and significantly higher rental vacancy rates compared to
  other clusters. This could indicate a more transient population or economic factors to consider.

### Cluster 2

- **Success Score**: Second-highest average success score (approximately 2.02), which also suggests successful Italian
  restaurants but to a slightly lesser extent than Cluster 3.
- **Housing Units**: The highest number of total housing units, with the majority being occupied. This cluster likely
  represents very populous areas with a large customer base.
- **Vacancy Rates**: Lowest homeowner vacancy rates among all clusters, indicating stable homeownership. Rental vacancy
  rates are higher than Cluster 1 but lower than Cluster 3.

### Cluster 1

- **Success Score**: Lower average success score (approximately 1.83), which may indicate areas with potential for
  growth or improvement in the restaurant industry.
- **Housing Units**: Lower total housing units than Cluster 2 but higher than Cluster 3, with a good percentage of
  occupied units.
- **Vacancy Rates**: The lowest rental vacancy rate, suggesting a strong rental market, which could be associated with
  younger demographics or urban settings.

### Cluster 0

- **Success Score**: The lowest average success score (approximately 1.59), indicating areas where Italian restaurants
  may struggle or have untapped potential.
- **Housing Units**: The highest number of vacant housing units, which could suggest economic challenges or a changing
  neighborhood demographic.
- **Vacancy Rates**: Moderate homeowner and rental vacancy rates. The high number of vacant units could be indicative of
  a less stable market for new ventures.

### Project Implications:

- **Most Favorable Locations**: Cluster 3, with the highest success score and a moderate number of occupied housing
  units, appears to be the most favorable for Italian restaurants. However, the high rental vacancy rate should be
  considered, as it might affect customer consistency.
- **Areas for Growth**: Cluster 1, with a lower success score but the lowest rental vacancy rate, could represent an
  opportunity for growth, targeting markets that are currently under-served.
- **Populous Markets**: Cluster 2 represents populous areas that already have a significant number of successful Italian
  restaurants, suggesting a competitive but potentially rewarding market.

    By combining these insights with additional local market research, you can make informed decisions on where to focus
    expansion efforts or where to look for untapped opportunities within the state of Pennsylvania for new Italian
    restaurant locations.

### Results from DP05 - 

## Chi-Square Test: 
   Useful for categorical data, this test can help you determine if the distribution of Italian restaurants across
   different categories (such as areas with different levels of access to public transportation) is different from what 
   would be expected by chance. For example, if Italian restaurants are more common in areas with high public 
   transportation access than expected, this factor might be important for location planning.

## ANOVA (Analysis of Variance): 
   Use this to compare means across different groups (such as zip codes with low,
   medium, and high median incomes) to determine if the differences in restaurant success measures across these groups
   are statistically significant. For example, ANOVA could tell you if the average revenue of Italian restaurants
   significantly differs across these income groups, indicating the importance of income level in site selection.

The order of these tests provides a progression from simple univariate analysis to more complex multivariate analysis,
allowing for a comprehensive understanding of the data. By starting with simpler tests, you can eliminate factors that
show little to no univariate relationship with your outcome of interest before moving on to more complex analyses that
consider multiple factors simultaneously.

