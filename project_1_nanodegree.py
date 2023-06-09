# -*- coding: utf-8 -*-
"""Project_1_Nanodegree.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xjhcewc7w4rYGJ7dF7y0Sybb4-r-fOEs
"""

import pandas as pd
import numpy as np
import seaborn as sns
import math
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

import warnings

warnings.filterwarnings("ignore")

calendar = pd.read_csv('calendar.csv')
listings = pd.read_csv('listings.csv')
reviews =  pd.read_csv('reviews.csv')

"""## Motivation
The aim of this project is to find the correlation between the prices of accommodations in Airbnb Seattle and factors such as location, size, amenities offered, and other relevant characteristics. Additionally, it seeks to identify the factors that influence host ratings and their relationship with guest satisfaction.

## Questions

1. What is the correlation between accommodation prices and factors such as location, size, capacity, amenities offered, among others?

2. What are the key factors that influence the review scores given by guests to the listings?

3. What is the expected review score for listings without an assigned score, and how reliable is the estimation?

## Description of the Data Used

This project is based on the following datasets from Airbnb Seattle:
- **Listings**: Contains detailed information about Airbnb properties in Seattle, such as price, location, size, and amenities offered.
- **Calendar**: Provides information about availability and daily prices of Airbnb properties in Seattle.

# Initial exploration 

An initial exploration of the Listings and Calendar datasets from the Airbnb Seattle Dataset will be conducted. The objective is to understand their content, identify the variables they contain, and select the variables relevant to the questions we have posed for further processing and cleaning. This selection will be crucial in order to obtain meaningful and accurate results during data analysis
"""

# Vista inicial
listings.head(5)

# Columnas y filas
listings.shape

# Tipos de datos
listing_type = pd.DataFrame(listings.dtypes)
listing_type

# Valores faltantes por columna
listing_null = pd.DataFrame(listings.isna().sum()).sort_values(0, ascending = False).head(50)
listing_null

# Vista inicial
calendar.head(5)

# Columnas y filas
calendar.shape

# Tipos de datos
calendar_type =  pd.DataFrame(calendar.dtypes)
calendar_type

# Valores faltantes por columna
calendar_null = pd.DataFrame(calendar.isna().sum()).sort_values(0, ascending = False).head(50)
calendar_null

"""## Remark 

The exploration begins with a preliminary overview of the datasets, allowing us to understand their content and get an idea of their structure. We examine the sizes of the datasets, data types, and null values. During the initial exploration, we notice that the datasets contain various types of data. However, it is necessary to correct the format for columns representing dates or prices. Additionally, we observe missing values in certain columns: "last_review" has 627 missing values, "neighbourhood" has 416, and "space" has 569 in the Listings dataset. In the Calendar dataset, the "price" column has 459,028 missing values. Now, we proceed to treat the data to achieve a cleaner foundation. Stay tuned for the upcoming steps!

# Cleaning and Data Processing

In this crucial section, we undertake meticulous variable selection closely aligned with our research questions. Our focus lies in correcting the formats of existing variables and creating meaningful new variables, such as semester, density, and price variation by semester. Additionally, we rigorously address missing values by imputing them based on the nature of each variable. This rigorous process ensures a solid and reliable data analysis. Join us as we explore and extract valuable insights from our dataset.

## Variable Selection

Firstly, we identify the variables related to each question, and then we will analyze the data quality of these columns, ensuring their consistency and completeness to obtain the most reliable foundation.

1. Question 1: Correlation between accommodation prices and factors such as location, space size, and offered amenities.

Variables of interest: "price" (accommodation price), "neighbourhood" (neighborhood), "accommodates" (accommodation capacity), "bedrooms" (number of bedrooms), "bathrooms" (number of bathrooms), "amenities" (offered amenities).

2. Question 2: Key factors influencing host ratings and their relationship with guest satisfaction.

Variables of interest: "review_scores_rating" (host rating score), "review_scores_accuracy" (accuracy rating), "review_scores_cleanliness" (cleanliness rating), "review_scores_communication" (communication rating), "review_scores_value" (value rating), "review_scores_location" (location rating).

3. Question 3: Expected review_scores_value for sites without this data recorded.

Variables of interest: All variables involved in questions 1 and 2.
"""

calendar['price'] = calendar['price'].str.replace('$', '').str.replace(',', '').astype('float') 
calendar['date'] = pd.to_datetime(calendar['date'])
calendar['available'] = calendar['available'].apply(lambda x: 1 if x == 't'  else 0)

# Verificación
calendar.head(5)

"""### Remark

The creation of the **"semestre"** variable in the analysis of the Airbnb dataset allows for dividing the places into semestral periods, which is beneficial for conducting comparisons and evaluating possible patterns in prices. This variable facilitates data segmentation and understanding, providing valuable information for informed decision-making in the temporary rental market.
"""

# creación de la variable semestre que nos permite identificar en que semestre del año se tiene el registro 
calendar['semestre'] = calendar['date'].apply(lambda x: 1 if x.month <= 6 else 2)

calendar

# Calcular el promedio de los precios por semestre
promedio_semestre = calendar.groupby([ calendar['date'].dt.month])['price'].mean().reset_index()

# Crear la gráfica de serie de tiempo
plt.figure(figsize=(10, 6))
plt.plot(promedio_semestre['date'], promedio_semestre['price'], label='avg_price_month')
plt.axvline(6, color='red', linestyle='--', label = 'June')

plt.xlabel('Mes')
plt.ylabel('Precio promedio')
plt.title('Promedio de precios')
plt.legend()
plt.show()

"""### Remark

The analysis of the graph reveals that during the first semester of the year, the average prices show a consistent increasing trend. However, in the second semester, the price behavior is more variable, reaching a peak between July and August, and reaching a minimum between October and November. These findings suggest that the price behavior differs significantly in each semester, highlighting the importance of considering semestral periods when analyzing prices in the Airbnb temporary rental market.
"""

# Divisón de la información por semestre
calendar_sem1 = calendar.query('semestre == 1')
calendar_sem2 = calendar.query('semestre == 2')

print(calendar_sem1.shape, calendar_sem2.shape)

# Resumen de la información por semestre
calendar_agg_sem1 = calendar_sem1.groupby('listing_id').agg({
    'listing_id': 'first',
    'available': ['sum', 'mean'],
    'price': ['min','max','mean']
})

calendar_agg_sem2 = calendar_sem2.groupby('listing_id').agg({
    'listing_id': 'first',
    'available': ['sum', 'mean'],
    'price': ['min','max','mean']
})

calendar_agg_sem1.columns = ['listing_id', 'dias_disponible_sem1', 'porc_disponible_sem1', 'price_min_sem1', 'price_max_sem1', 'price_avg_sem1' ] 
calendar_agg_sem1['variacion_precio_sem1'] = calendar_agg_sem1['price_max_sem1'] - calendar_agg_sem1['price_min_sem1'] 
calendar_agg_sem2.columns = ['listing_id2', 'dias_disponible_sem2', 'porc_disponible_sem2', 'price_min_sem2', 'price_max_sem2', 'price_avg_sem2' ] 
calendar_agg_sem1['variacion_precio_sem2'] = calendar_agg_sem2['price_max_sem2'] - calendar_agg_sem2['price_min_sem2']

calendar_agg_sem = calendar_agg_sem1.merge(calendar_agg_sem2, right_on= calendar_agg_sem2['listing_id2'] , left_on = calendar_agg_sem1['listing_id'], how = 'inner')[['listing_id', 'dias_disponible_sem1', 'porc_disponible_sem1',
       'price_min_sem1', 'price_max_sem1', 'price_avg_sem1', 'variacion_precio_sem1' ,'dias_disponible_sem2', 'porc_disponible_sem2', 'price_min_sem2', 'price_max_sem2', 'price_avg_sem2', 'variacion_precio_sem2']]

calendar_agg_sem

calendar_agg_sem.isna().sum()

calendar_agg_sem.describe()

"""### Remark

#### For Semester 1:

*  **Days Available**: On average, accommodations were available for approximately $119$ days, representing around $65.9\%$ of the semester.
* **Minimum Price**: The minimum price recorded during Semester 1 was $\$117$.
* **Maximum Price**: The maximum price reached during Semester 1 was $\$155$.
* **Average Price**: The average price during Semester 1 was around $\$133$.
* **Price Variation**: The price variation within Semester 1 was approximately $\$38.18$.

#### For Semester 2:

* **Days Available**: On average, accommodations were available for about $125$ days, representing approximately $68.2\%$ of the semester.
* **Minimum Price**: The minimum price recorded during Semester 2 was $\$133$.
* **Maximum Price**: The maximum price reached during Semester 2 was $\$162$.
Average Price: The average price during Semester 2 was around $\$145$.
* **Price Variation**: The price variation within Semester 2 was approximately $\$29.71$.

These data suggest that, on average, accommodations have higher availability in Semester 2 compared to Semester 1. Additionally, prices in Semester 2 appear to be slightly higher overall, with lower price variation compared to Semester 1.

## Join datasets

1. The variable "density" summarizes the number of listings in the vicinity of each property. It is classified as high density if there are more than $100$ listings, medium density if there are between $100$ and $50$ listings, and low density if there are less than $50$ listings. This variable is important for analyzing the competition and demand for Airbnb accommodations in different locations.

2. The variable "amenities count" represents the quantification of the amenities provided by the property. It is interesting to include this variable in the analysis as amenities can significantly impact the attractiveness and satisfaction of guests. The more amenities a property offers, the more appealing it is likely to be to potential renters, enhancing their overall experience. By considering the count of amenities available, we gain a quantitative measure that helps assess the value and desirability of each accommodation within the Airbnb market.
"""

cols = ['id', 'price', 'neighbourhood', 'accommodates', 'bedrooms', 'bathrooms', 'amenities', 'cancellation_policy', 'room_type',
        'review_scores_rating', 'review_scores_accuracy', 'review_scores_cleanliness', 'review_scores_communication', 'review_scores_value', 'review_scores_location',
        'availability_365', 'dias_disponible_sem1', 'porc_disponible_sem1',
       'price_min_sem1', 'price_max_sem1', 'price_avg_sem1', 'variacion_precio_sem1',
       'dias_disponible_sem2', 'porc_disponible_sem2', 'price_min_sem2',
       'price_max_sem2', 'price_avg_sem2', 'variacion_precio_sem2']

df = listings.merge(calendar_agg_sem, left_on = listings.id, right_on = calendar_agg_sem.listing_id,how = 'left')[cols]

df.drop_duplicates(inplace=True)

df['amenities_count'] = df['amenities'].apply(lambda x: len(x.split(',')))

densidad = pd.DataFrame(df.neighbourhood.value_counts())
densidad['densidad'] = pd.DataFrame(df.neighbourhood.value_counts())['neighbourhood'].apply(lambda x: 'densidad_alta' if x > 100 else 'densidad_media' if x < 100 and x > 49 else 'bajo')
densidad = densidad.reset_index()
densidad.columns = ['neighbourhood', 'conteo', 'densidad']
densidad

var = list(df.columns)
var.append('densidad')

df = df.merge(densidad, left_on='neighbourhood', right_on='neighbourhood', how='left')[var]

df['price'] = df['price'].str.replace('$', '').str.replace(',', '').astype('float')

df.isna().sum()

"""### Last exploration 

This is the final phase of data cleaning, preprocessing, and exploration to ensure a clean dataset for further analysis. Firstly, a selection of variables is made in two categories. 
1. Variables related to price are chosen based on correlation matrix. 
2. Variables related to availability are also selected using the correlation matrix.

Additionally, missing values in the "bedrooms" and "bathrooms" variables are filled with a value of 1. Missing values in price variation variables are filled with 0, and the density variable is marked as unknown.
"""

def corr_matrix_plot(dataframe, variables, title):
    """
    Creates a heatmap that displays the correlation matrix between the specified variables.

    Inputs:
    - dataframe: pandas DataFrame. 
    - variables: list of strings. 
    - title: string. 

    Output:
    Displays a heatmap of the correlation matrix.
        """

    # Calculate the correlation matrix
    corr_matrix = dataframe[variables].corr()

    # Visualize the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title(title)
    plt.show()

def box_plot(dataframe, x_var, y_var, x_label, y_label, title):
    """
     Creates a heatmap that displays the boxplot between the specified variables.

    Parameters:
    - dataframe: pandas DataFrame. The dataset from which the box plot will be created.
    - x_var: string. The name of the variable to be plotted on the x-axis.
    - y_var: string. The name of the variable to be plotted on the y-axis.
    - x_label: string. The label for the x-axis.
    - y_label: string. The label for the y-axis.
    - title: string. The title to be displayed on the box plot.

    Output:
    Displays a customized box plot.
    """

    plt.figure(figsize=(8, 6))
    sns.boxplot(data=dataframe, x=x_var, y=y_var)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x='bedrooms', y='price')
plt.xlabel('Número de habitaciones')
plt.ylabel('Precio del alojamiento')
plt.title('Correlación entre precio y número de habitaciones')
plt.show()

corr_matrix_plot(df, ['price', 'price_min_sem1', 'price_max_sem1', 'price_avg_sem1', 'variacion_precio_sem1', 'price_min_sem2', 'price_max_sem2', 'price_avg_sem2', 'variacion_precio_sem2' ], 'Matriz de correlación')

corr_matrix_plot(df, ['availability_365', 'dias_disponible_sem1', 'dias_disponible_sem2', 'porc_disponible_sem1', 'porc_disponible_sem2' ], 'Matriz de correlación')

"""**Finally**, the variables 'amenities', 'neighbourhood', 'price_min_sem1', 'price_max_sem1', 'price_avg_sem1', 'price_min_sem2', 'price_max_sem2', and 'price_avg_sem2' are removed.

With this resulting dataset, the subsequent questions and analyses will be conducted.
"""

df.drop(['amenities', 'neighbourhood', 'price_min_sem1', 'price_max_sem1', 'price_avg_sem1','price_min_sem2', 'price_max_sem2', 'price_avg_sem2',], axis = 1, inplace = True)

df['bedrooms'] = df['bedrooms'].fillna(1) 
df['bathrooms'] = df['bathrooms'].fillna(1) 
df['variacion_precio_sem1'] = df['variacion_precio_sem1'].fillna(0) 
df['variacion_precio_sem2'] = df['variacion_precio_sem2'].fillna(0)
df['densidad'] = df['densidad'].fillna('sin_info')

df['bathrooms'] = df['bathrooms'].apply(lambda x: math.ceil(x))

df.head(5)

"""## Questions solution

1. What is the correlation between accommodation prices and factors such as location, size, capacity, amenities offered, among others?

To address our first question, we will follow these steps in analyzing the dataset:

Price distribution: We will investigate the distribution of prices to understand how they are spread across the dataset.

Exploratory analysis of variables: We will explore the variables "bedrooms," "accommodates," "bathrooms," "density," and "amenities count." We will analyze their distributions, descriptive statistics, and potential relationships with price.

Correlation matrix with respect to price: We will calculate the correlation matrix between all variables and price. We will examine the correlations to identify possible influences and significant relationships with price.

With these analyses, we aim to gain insights into the price distribution and explore how the variables "bedrooms," "accommodates," "bathrooms," "density," and "amenities count" relate to price within the dataset.
"""

# Análisis exploratorio de datos y visualización
# Graficar la relación entre el precio y el tamaño del espacio
plt.figure(figsize=(8, 6))
plt.hist(df['price'], bins = 20)
plt.ylabel('Conteo')
plt.xlabel('Precio del alojamiento')
plt.title('Distribución de los precios')
plt.show()

resumen = pd.DataFrame(df['price'].describe())
resumen

"""### Remark


The average price of accommodations in Seattle is approximately $\$128$ USD, with significant variability in prices (standard deviation of $\$90.25$). Most accommodations have affordable prices, with $50\%$ of them priced below $\$100$ USD. However, there are also more luxurious options available, with a maximum price of $\$1000$ USD.


"""

# Análisis exploratorio de datos y visualización
# Graficar la relación entre el precio y el tamaño del espacio
box_plot(df, 'bedrooms', 'price','Número de habitaciones' , ' Precio del alojamiento' ,'Correlación entre precio y número de habitaciones')

df.groupby('bedrooms').agg({'price':['mean', 'std', 'count' ]}).sort_values(('price','mean'))

"""### Remark
The number of bedrooms in an accommodation in Seattle is related to the price charged. In general, it is observed that as the number of bedrooms increases, the average price also tends to increase. For example, accommodations with 1 bedroom have an average price of around $\$96$ USD, while those with 6 bedrooms have a higher average price of approximately $\$578$ USD. This pattern suggests that the size and capacity of the accommodation influence the expected price to be paid.
"""

# Graficar la relación entre el precio y el tamaño del espacio
box_plot(df, 'accommodates', 'price','Capacidad de alojamiento' , ' Precio del alojamiento' ,'Correlación entre precio y capacidad de alojamiento')

df.groupby('accommodates').agg({'price':['mean', 'std', 'count' ]}).sort_values(('price','mean'))

"""### Remark 


The accommodation capacity has a relationship with the price in Seattle. It is observed that as the accommodation capacity increases, the average price also tends to increase. For example, accommodations for 1 person have an average price of around $\$58$ USD, while those with a capacity of 11 people have a higher average price of approximately $\$567$ USD. This pattern suggests that the accommodation capacity influences the expected price to be paid, as larger accommodations tend to be more expensive. However, it is important to note that as the accommodation capacity increases, the availability of listings decreases.
"""

# Graficar la relación entre el precio y el número de baños
box_plot(df, 'bathrooms', 'price','Número de baños' , ' Precio del alojamiento' ,'Correlación entre precio y número de baños')

df.groupby('bathrooms').agg({'price':['mean', 'std', 'count' ]}).sort_values(('price','mean'))

"""### Remark

The number of bathrooms in an accommodation is also related to the price in Seattle. In general, it is observed that as the number of bathrooms increases, the average price tends to increase. For example, accommodations with 1 bathroom have an average price of around $\$106$ USD units, while those with 5 bathrooms have a higher average price of approximately $\$352$ USD. This indicates that the number of bathrooms is a factor that influences the accommodation price.
"""

# Graficar la relación entre el precio y el número de baños

box_plot(df, 'densidad', 'price','Densidad' , ' Precio del alojamiento' ,'Correlación entre precio y densidad')

df.groupby('densidad').agg({'price':['mean', 'std', 'count' ]}).sort_values(('price','mean'))

# Graficar la relación entre el precio y el número comodidades
box_plot(df, 'amenities_count', 'price','Número de comodidades' , ' Precio del alojamiento' ,'Número de comodidades y número de comodidades')

df.groupby('amenities_count').agg({'price':['mean', 'std', 'count' ]}).sort_values(('price','mean'))

"""#### Remark 

The number of amenities offered in an accommodation is also related to the price in Seattle. As the number of amenities increases, the average price tends to increase. For example, accommodations that offer 7 amenities have an average price of around $\$86$ USD, while those that offer 27 amenities have a higher average price of approximately $\$196$ USD units. This suggests that the number of amenities available in an accommodation influences its price.
"""

# Calcular la correlación entre variables

corr_matrix_plot(df, ['price', 'accommodates', 'bedrooms', 'bathrooms', 'amenities_count'], 'Matriz de correlación')

"""# Conclusion

There is a positive correlation between the price of accommodations and factors such as the size of the space (number of bedrooms and bathrooms) and the accommodation capacity. The strongest correlation is observed between price and accommodation capacity, followed by the correlation with the size of the space. This indicates that, in general, as the size of the space and the accommodation capacity increase, the price tends to be higher.

On the other hand, the correlation between price and the number of amenities offered is relatively low, suggesting that the amenities offered do not have a significant influence on the price of accommodations. However, it is important to note that this correlation is based on the analyzed data and there may be other unconsidered factors that also affect the price.

In conclusion, the location, size of the space, and accommodation capacity are important factors to consider when determining the price of accommodations in Seattle.

2. What are the key factors that influence the review scores given by guests to the listings?

The plan of action for developing the second question:

* **Variables**: We will analyze the influence of the following variables on the review scores given by guests: 'review_scores_accuracy', 'review_scores_cleanliness', 'review_scores_communication', 'review_scores_value', and 'review_scores_location'.

* **Missing values**: It is important to note that these variables have missing values. However, we will still use the available data for analysis. This is justified because even though there are missing values, analyzing the correlation with the available data can still provide valuable insights and help us draw reliable conclusions.

* **Correlation analysis**: We will focus on the variable 'review_scores_value' and examine its correlation with the other variables mentioned above. By analyzing the correlation matrix, we can identify the key factors that have a significant influence on the review scores given by guests. This will allow us to determine which aspects of the listings are most important in terms of guest satisfaction and perception.

By following this plan of action, we can gain insights into the key factors that influence the review scores given by guests to the listings, even with the presence of missing values.
"""

scores = ['review_scores_accuracy', 'review_scores_cleanliness',
       'review_scores_communication', 'review_scores_value',
       'review_scores_location']

df_scores = df[scores]

df_scores.describe()

df_scores.isna().sum()/df_scores.shape[0]

corr_matrix_plot(df,scores, 'Matriz de correlación')
#corr_matrix = df_scores.corr()

"""## Conclusion

The correlation between the review scores is as follows:

1. There is a moderate positive correlation between the accuracy score and the cleanliness score $(0.54)$, communication score $(0.42)$, value score $(0.56)$, and location score $(0.26)$. This indicates that hosts who receive high accuracy scores tend to also receive high scores in these other aspects.

2. There is a moderate positive correlation between the cleanliness score and the communication score $(0.38)$, value score $(0.52)$, and location score $(0.27)$. This suggests that hosts who maintain clean accommodations tend to have good communication, offer good value, and are located in favorable areas.

3. There is a moderate positive correlation between the communication score and the value score $(0.46)$. This indicates that hosts who effectively communicate with their guests also provide good value in relation to the price paid.

4. The location score shows a moderate positive correlation with the value score $(0.36)$. This suggests that well-located accommodations tend to offer good value to guests.

In summary, the review scores are positively correlated, indicating that hosts who excel in one aspect tend to excel in other aspects as well. Accuracy, cleanliness, communication, value, and location are key factors influencing the overall rating of hosts.

3.  What is the expected review score for listings without an assigned score, and how reliable is the estimation?

### Solution

The process to answer the question is as follows:

1. **Variable selection**: Relevant variables are chosen based on prior experience.
2. **Missing value imputation**: For score variables like "review_scores_accuracy" and "review_scores_cleanliness" with missing values, imputation is performed using the average based on grouping "room_type" and "accommodates," excluding the review score to be estimated.
3.**Dataset split**: The dataset is divided into two sets, one containing records with non-null review scores and the other for estimating the "review_scores_value."
4. **Treatment of categorical variables**: Dummy variable encoding is applied to categorical variables like "cancellation_policy," "density," and "room_type," dropping the first dummy column to avoid multicollinearity.
5. **Regression model**: A regression model is built with "review_scores_value" as the target variable. StandardScaler is used for feature scaling, and multiple models are trained. The best model is selected based on metrics such as $R^2$ and $RMSE$.
6. **Estimation evaluation**: The reliability of the estimation is assessed using performance metrics from the chosen model.

In conclusion, this process aims to estimate the expected review score for listings without an assigned score. The reliability of the estimation is evaluated using selected performance metrics.
"""

vars = ['price', 'accommodates', 'bedrooms', 'bathrooms', 'cancellation_policy', 'room_type', 'review_scores_rating',  'review_scores_accuracy', 'review_scores_cleanliness',
       'review_scores_communication', 'review_scores_value','review_scores_location', 'availability_365', 'variacion_precio_sem1', 'variacion_precio_sem2', 'amenities_count', 'densidad']

df1 = df[vars]

df1['review_scores_accuracy_filled'] = df1.groupby(['room_type', 'accommodates'])['review_scores_accuracy'].transform(lambda x: x.fillna(x.mean()))
df1['review_scores_cleanliness_filled'] = df1.groupby(['room_type', 'accommodates'])['review_scores_cleanliness'].transform(lambda x: x.fillna(x.mean()))
df1['review_scores_rating_filled'] = df1.groupby(['room_type', 'accommodates'])['review_scores_rating'].transform(lambda x: x.fillna(x.mean()))
df1['review_scores_communication_filled'] = df1.groupby(['room_type', 'accommodates'])['review_scores_communication'].transform(lambda x: x.fillna(x.mean()))
df1['review_scores_location_filled'] = df1.groupby(['room_type', 'accommodates'])['review_scores_location'].transform(lambda x: x.fillna(x.mean()))

df1.drop(['review_scores_rating',  'review_scores_accuracy', 'review_scores_cleanliness','review_scores_communication','review_scores_location'], axis = 1, inplace = True)

df1.isna().sum()

# Lista de variables a convertir en variables dummies
variables_dummies = ['cancellation_policy', 'densidad', 'room_type']

# Aplica la conversión a variables dummies eliminando la primera categoría
df_dummies = pd.get_dummies(df1[variables_dummies], drop_first=True)

# Concatena las variables dummies al DataFrame original
df1 = pd.concat([df1, df_dummies], axis=1)

# Elimina las columnas originales
df1.drop(variables_dummies, axis=1, inplace=True)

df_model = df1.query('~ review_scores_value.isna()')
df_estimar = df1.query(' review_scores_value.isna()')

var_x = ['price', 'accommodates', 'bedrooms', 'bathrooms',
       'availability_365', 'variacion_precio_sem1', 'variacion_precio_sem2',
       'amenities_count', 'review_scores_accuracy_filled',
       'review_scores_cleanliness_filled', 'review_scores_rating_filled',
       'review_scores_communication_filled', 'review_scores_location_filled',
       'cancellation_policy_moderate', 'cancellation_policy_strict',
       'densidad_densidad_alta', 'densidad_densidad_media',
       'densidad_sin_info', 'room_type_Private room', 'room_type_Shared room']

X = df_model[var_x]

y = df_model['review_scores_value']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Creación y ajuste del modelo de regresión lineal
model = LinearRegression()
model.fit(X_train, y_train)

# Predicción de los valores para los registros sin score
y_pred = model.predict(X_test)

# Evaluación del modelo
mse = mean_squared_error(y_test, y_pred)
r2 = model.score(X_test, y_test)

print('Error cuadrático medio (MSE):', mse)
print('Coeficiente de determinación (R2):', r2)

X_estimar = df_estimar[var_x]
X_estimar_scaler = scaler.transform(X_estimar)

print('mean:', model.predict(X_estimar_scaler).mean(), 'max:',model.predict(X_estimar_scaler).max(), 'min:',model.predict(X_estimar_scaler).min())

coef = pd.DataFrame({'Variable': var_x, 'Coef':model.coef_}).sort_values('Coef')
coef

X_filtered = df_model[['bedrooms', 'review_scores_accuracy_filled',
       'review_scores_cleanliness_filled', 'review_scores_rating_filled',
       'review_scores_communication_filled', 'review_scores_location_filled']]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_filtered)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Creación y ajuste del modelo de regresión lineal
model2 = LinearRegression()
model2.fit(X_train, y_train)

# Predicción de los valores para los registros sin score
y_pred = model2.predict(X_test)

# Evaluación del modelo
mse = mean_squared_error(y_test, y_pred)
r2 = model2.score(X_test, y_test)

print('Error cuadrático medio (MSE):', mse)
print('Coeficiente de determinación (R2):', r2)

X_estimar = df_estimar[['bedrooms', 'review_scores_accuracy_filled',
       'review_scores_cleanliness_filled', 'review_scores_rating_filled',
       'review_scores_communication_filled', 'review_scores_location_filled']]

X_estimar_scaler = scaler.transform(X_estimar)

print('mean:', model2.predict(X_estimar_scaler).mean(), 'max:',model2.predict(X_estimar_scaler).max(), 'min:',model2.predict(X_estimar_scaler).min())

"""# Results and Conclusions:

Several linear regression models were trained, and the following metrics were obtained for two of the models:

* Model 1:
Mean Squared Error (MSE): 0.29835273989400485
Coefficient of Determination (R2): 0.48333191721242574

* Model 2:
Mean Squared Error (MSE): 0.30147789332369734
Coefficient of Determination (R2): 0.47791997753488213

For the **Model 1**, the variables 'price', 'accommodates', 'bedrooms', 'bathrooms', 'availability_365', 'variacion_precio_sem1', 'variacion_precio_sem2', 'amenities_count', 'review_scores_accuracy_filled', 'review_scores_cleanliness_filled', 'review_scores_rating_filled', 'review_scores_communication_filled', 'review_scores_location_filled', 'cancellation_policy_moderate', 'cancellation_policy_strict', 'densidad_densidad_alta', 'densidad_densidad_media', 'densidad_sin_info', 'room_type_Private room', and 'room_type_Shared room' were used.

The second model considered the five most significant variables based on their coefficients. These variables are as follows:

| Variable |  coeficiente |
|:-----------:|:-----------:|
| review_scores_rating_filled   | 0.339950  |
| review_scores_accuracy_filled  | 0.124079  |
| review_scores_location_filled  | 0.094497  |
| review_scores_communication_filled  | 0.066586  |
| review_scores_cleanliness_filled  | 0.051425  |
| bedrooms  | 0.048369 |


The coefficients indicate the strength and direction of the relationship between the variables and the review_scores_value.

Additionally, **Model 2** was trained using the six variables with the highest coefficients


The estimated review score ranges for both models were found to be consistent, with Model 1 having a:
1. mean score of 9.478455749390402.
2. maximum of 9.993691433177814
3. minimum of 7.981734469207332. 

With Model 2:  
1. mean score of 9.447350049991456
2. maximum of 9.901933492509643
3. minimum of 7.821843108572441.

It is important to note that while the estimated score ranges are consistent, there is room for improvement in the models. Further refinement and exploration of additional variables could lead to more accurate estimations.

In conclusion, the models provide estimations for the review_scores_value, and the ranges of the estimated scores are consistent. However, there is potential for improvement, and further analysis and inclusion of other relevant variables may enhance the accuracy of the estimations.
"""