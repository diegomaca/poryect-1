# Airbnb Seattle Project: Price Analysis, Rating Factors, and Review Score

## Installation and Libraries
- Python
- NumPy
- Seaborn
- Matplotlib
- Scikit-learn
## Motivation
The aim of this project is to find the correlation between the prices of accommodations in Airbnb Seattle and factors such as location, size, amenities offered, and other relevant characteristics. Additionally, it seeks to identify the factors that influence host ratings and their relationship with guest satisfaction.

## Questions

1. What is the correlation between accommodation prices and factors such as location, size, capacity, amenities offered, among others?

2. What are the key factors that influence the review scores given by guests to the listings?

3. What is the expected review score for listings without an assigned score, and how reliable is the estimation?

## Description of the Data Used
This project is based on the following datasets from Airbnb Seattle in archive.zip:
- **Listings**: Contains detailed information about Airbnb properties in Seattle, such as price, location, size, and amenities offered.
- **Calendar**: Provides information about availability and daily prices of Airbnb properties in Seattle.

## Project Description
The project is divided into the following stages:

### Exploration
In this stage, the Airbnb Seattle datasets (Listings and Calendar) will be loaded for further analysis. Data completeness, consistency, and variable selection related to the posed questions will be explored.

### Data Cleaning and Treatment
A thorough data cleaning process will be conducted, including the removal of outliers, format correction, and handling missing values. Furthermore, data will be processed to prepare it adequately for analysis.

### Exploratory analisys
In the exploratory analysis, various explorations and visualizations of the data were conducted to gain a better understanding of the characteristics and distributions of the relevant variables in the Airbnb Seattle dataset. Variables such as prices, accommodation capacity, number of bedrooms and bathrooms, as well as the quantity of amenities offered, were examined.

A correlation analysis was also performed on the numerical variables, such as prices, accommodation capacity, and the number of bedrooms and bathrooms. This analysis was visualized using a heatmap, which allowed for the identification of possible relationships and dependencies among these variables.

### Modeling
In this stage, techniques for exploratory data analysis and statistical modeling will be applied to find the correlation between accommodation prices and the considered factors. The factors influencing host ratings and their relationship with guest satisfaction will be identified. Linear regression techniques will be employed to predict the expected review score for listings without an assigned score.

## Summary of the results

The detailed analysis and findings of this study can be found in the following link:
https://medium.com/@diego.maca/exploratory-analysis-with-python-of-accommodation-prices-and-factors-influencing-review-scores-in-6010a52447fa .

In this section, we provide a concise summary of the results obtained from the analysis.

1. Accommodation Prices: A positive correlation was found between accommodation prices and factors such as size (number of bedrooms and bathrooms) and accommodation capacity. Additionally, the number of amenities offered also influences the price. These factors are important in determining the prices of accommodations in Seattle.

2. Key Factors Influencing Review Scores: The key factors that influence review scores given by guests were identified. Accuracy, cleanliness, communication, value, and location are significant factors that influence review scores. Hosts who receive high scores in one of these aspects tend to receive high scores in other aspects as well. These factors are crucial for guest satisfaction and perception.

3. Estimation of Review Scores: Linear regression models were developed to estimate review scores based on various variables. Consistent estimations for review scores were obtained, although there are areas for improvement, and the inclusion of additional variables could enhance the accuracy of the estimations.

## Acknowledgment:

For the dataset from Kaggle:
Kaggle. (n.d.). Seattle Airbnb Open Data. Retrieved from https://www.kaggle.com/datasets/airbnb/seattle

For the article on the CRISP-DM methodology:
Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., ... & Wirth, R. (2000). CRISP-DM 1.0: Step-by-step data mining guide. Retrieved from https://www.datascience-pm.com/crisp-dm-2/

For the classes in Module 1 of the Udacity Data Scientist Nanodegree Program:
Udacity. (n.d.). Data Scientist Nanodegree Program. Module 1: Introduction to Data Science. Retrieved from [link to the course](https://learn.udacity.com/nanodegrees/nd002/parts/cd0000)](https://learn.udacity.com/nanodegrees/nd025)]([link to the course](https://learn.udacity.com/nanodegrees/nd025)

## License MIT License

## Authors
Diego Maca
