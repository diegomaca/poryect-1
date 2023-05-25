# Proyecto Airbnb Seattle: Análisis de Precios, Factores de Calificación y Review Score

## Instalaciones y librerías
- Python
- NumPy
- Seaborn
- Matplotlib
- Scikit-learn

## Motivación
El objetivo de este proyecto es encontrar la correlación entre los precios de los alojamientos en Airbnb Seattle y factores como la ubicación, el tamaño, las comodidades ofrecidas entre otras caracteristicas. También se busca identificar los factores que influyen en la calificación de los anfitriones y cómo se relaciona con la satisfacción de los huéspedes.

Teniendo esto en mente, se plantean las siguientes preguntas:

1. Cuál es la correlación entre el precio de los alojamientos y factores como la ubicación, el tamaño, la capacidad, las comodidades ofrecidas entre otros aspectos?

2. ¿Cuáles son los factores clave que influyen en el **review_score** que dan los huespedes a los lugares ?

3. ¿Cuál es el **reviewe_score** esperado para los lugares que no tienen puntaje asignado y que tan confiable puede ser la estimación?

## Descripción de los datos utilizados
Este proyecto se basa en los siguientes conjuntos de datos de Airbnb Seattle:
- **Listings**: Contiene información detallada sobre las propiedades de Airbnb en Seattle, como el precio, la ubicación, el tamaño y las comodidades ofrecidas.
- **Calendar**: Contiene información sobre la disponibilidad y los precios diarios de las propiedades de Airbnb en Seattle.

## Descripción del proyecto
El proyecto se divide en las siguientes etapas:

### Exploración
En esta etapa, se cargarán los conjuntos de datos de Airbnb Seattle (Listings y Calendar) para su posterior análisis, donde se explora la completitud de los datos, su consistencia y se hace una selección apriori de las variables relacionadas con las preguntas que nos planteamos a partir de los datos.

### Limpieza y tratamiento de los datos
Se realizará una limpieza exhaustiva de los datos, incluyendo la eliminación de valores atípicos, la corrección de formatos y el manejo de valores faltantes. Además, se realizará un procesamiento de los datos para prepararlos adecuadamente para el análisis.

### Modelación
En esta etapa, se aplicarán técnicas de análisis exploratorio de datos y modelado estadístico para encontrar la correlación entre los precios de los alojamientos y los factores considerados. También se identificarán los factores que influyen en la calificación de los anfitriones y se analizará su relación con la satisfacción de los huéspedes. Se utilizarán técnicas de regresión lineal para predecir el review score esperado para los alojamientos que no tienen registrada esta calificación.

## Authors 
Diego Maca



