# Italy House Prices
This repository contains the code I have developed to produce house price prediction models.

The repository is structured as follows:
## 1_ingest
The folder contains the code required for data cleaning and feature engineering, specifically:
- 1_data_import_and_cleaning.ipynb: reads in immobiliare.it data and filters it to keep only sale related posts. Further, cleaning of different relevant variables is performed, such as: prezzo, m2, date, stanze, bagni, piani, cucina, disponibilità, tipologia casa, posti auto, other relevant characteristics. Duplicate observations are also dropped

- 2_feature_engineering.ipynb: expands the previously cleaned data by introducing population, income and other key aspects available in the house description. Data is also filtered on price and m2 to keep only the most relevant properties

## 2_eda
The folder contains the performed exploratory analysis, consisting of:
- 3_exploratory_data_analysis.ipynb: it segments the categorical variables based on their levels and plots the house price distribution in each of them. The house description embeddings are also plotted.

- 4_geographic_exploration.ipynb: exploits plotly to produce a summary graph of where houses are located in Italy in my cleaned dataset.

## 3_modelling
The modelling folder performs train-valid-test split, quantile regression and its evaluation and the final refitting.
- 5_train_valid_test_split.ipynb: splits the data into train, validation and test by stratifying on a combination of the following variables: price_bin, regione, stanze, bagni, tipologia_casa, classe_casa, tipologia_proprietà. Categorical variables are also encoded here.

- 6_quantile_modelling.ipynb: exploits ml_optfit to fit and optimize LightGBM and XGBoost quantile regressions. The quantiles predicted are: 0.05, 0.5, and 0.95. The first and the last are used to create a 90% prediction interval whereas the median prediction serves as a pin-point prediction. Model Stacking is also analyzed but as it would increase the modelling complexity and the container size it is discarded.

- 7_ml_evaluation.ipynb: analyzes the fit performance of the developed ML models by computing: RMSE, MAE, R2, Pinball score and MAPE for the pin-point price prediction. The coverage fraction is instead computed for the 0.05 and 0.95 quantile predictions. Finally, the feature importances are compured as well as the shap values for the top 20 features.

- 8_refit.ipynb: refits the best model on train+valid to identify generalizability on test data. Once that is verified, the model is finally re-trained on all the data available.

## 4_deploy_app
The folder contains the relevant files to create a working Docker container and Streamlit front-end interface.
- container_app.py: creates a prediction route for the Flask application of the model, serving as the model API.

- predict.py: contains the relevant code to translate raw data into house price predictions.

- streamlit_app.py: creates the streamlit front-end application to collect data and produce house price predictions.