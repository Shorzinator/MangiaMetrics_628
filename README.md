# Mangia Metrics

## Location of important files and folders

- The Presentation and Executive summary are both located in the root directory itself.
- The code for shiny app has also been added to the ShinyApp directory along with a README explaining the capabilities
  of our app.
- Now, regarding all other directories -

    - ./data - This directory contains three subdirectories -

        - ./final - This contains all the datasets that had been cleaned and preprocessed and required no possible
          interaction in terms of their content.
        - ./interim - This contains all the preprocessed and cleaned data, but the ones that were constantly being
          changed due to change in approach of cleaning, updates regarding some specific aspects of cleaning and
          preprocessing, etc.
        - ./raw - This contains all the raw data files, out of which many could not be uploaded to GitHub due to the
          limitations on size. We employed git lfs to try and stretch that limit, but not to a huge extent.

    - ./results - This directory contains results from our EDA and modeling

        - ./eda - This directory has two subdirectories. We performed our EDA in two phases - the first one was a more
          high level analysis whereas the second phase delved deeper into specific data sets -

            - ./Phase 1
            - ./Phase 2

        - ./modeling - This directory contains results from our ML models.

    - ./scripts - This directory contains all the python scripts -

        - ./data cleaning - As the name suggests, contains scripts that were used in the cleaning process. Contains
          separate scripts for some kinds of data but one comprehensive script for most of the datasets we operated on.
        - ./eda - This, once again, contains two subdirectories as part of our two phases of EDA
        - ./modeling - This contains scripts for our ML models and PCA.
        - ./utility - This contains utility functions that were used throughout the project to invoke relative path and
          load data without absolute path to make the project more robust and thus, can be run on different systems.
      
    - ./ShinyApp - Contains the script behind our shiny app and a readme explaining the functionalities of the app.


### Note: You can try to run any script on this project and it would run fine so long as all the dependencies are not detached.