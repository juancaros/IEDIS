------Implementación en Streamlit------
En el archivo francia-ansiedad.py favor cambiar línea 14 a 17
	Ejemplo, actualmente aparece un análisis para Francia y Ansiedad de la siguiente manera 
		country = "Francia"  
		country_h="France" 
		keyword = "Ansiedad"

	Para España y Depresión el cambio debe ser el siguiente:
		country = "España"  
		country_h="Spain" 
		keyword = "Depresión"

Los gráficos menos representativos puedes ser eliminados
----------------------------------------------------------------------------------------
Repositorio Alejandro

Este repositorio contiene herramientas para analizar datos de Google Trends utilizando la librería Prophet. Los datos cubren búsquedas semanales entre los años 2010 y 2023 para varios países y palabras clave relacionadas con temas de salud mental.

Contenido del repositorio
1. francia-ansiedad.py
Este código se basa en el enfoque presentado en el sitio web "https://juanitorduz.github.io/fb_prophet/" para usar Prophet en análisis de series temporales con datos de Google Trends semanales.

-Lee un archivo CSV con datos de Google Trends.
-Filtra los datos para un país específico (Francia) y una palabra clave (Ansiedad). Estos pueden ser cambiados para su implementación en streamlit
-Convierte las fechas del DataFrame a formato datetime.
-Obtiene los días festivos del país seleccionado y los almacena en un DataFrame.
-Prepara y ajusta el modelo Prophet.
-Define parámetros de crecimiento logístico.
-Divide los datos en conjuntos de entrenamiento y prueba.
-Configura el modelo Prophet con estacionalidad semanal y anual, y días festivos.
-Realiza predicciones futuras y devuelve el modelo ajustado, las predicciones y los datos de prueba.
-Evalúa el rendimiento del modelo calculando el error absoluto medio (MAE) y el error cuadrático medio (RMSE) entre las predicciones y los valores reales.
-Itera sobre diferentes órdenes de Fourier para la estacionalidad anual.
-Ajusta el modelo Prophet con cada orden y evalúa el rendimiento usando MAE y RMSE.
-Selecciona el modelo con el menor MAE para graficar las predicciones finales.
-Grafica las predicciones del modelo Prophet.
-Incluye líneas verticales para los días festivos.
-Muestra los componentes del modelo (tendencias y estacionalidades).
-Compara las predicciones con los valores reales, destacando el año 2023 si es relevante.

2. francia-ansiedad.py
Los países de la Unión Europea se han dividido en grupos basados en su ubicación geográfica, lo que facilita la comparación de tendencias entre regiones similares.
	Grupo 1: ["Alemania", "Austria", "Bélgica", "Países Bajos", "Luxemburgo"]
	Grupo 2: ["España", "Francia", "Italia", "Portugal", "Grecia"]
	Grupo 3: ["Finlandia", "Irlanda", "Malta", "Chipre", "Estonia"]
 	Grupo 4: ["Croacia", "Eslovaquia", "Eslovenia", "Letonia", "Lituania"]
Este algoritmo genera gráficos proporcionan una visualización clara de cómo las tendencias de búsqueda de "Ansiedad" y "Depresión" han variado en diferentes grupos de países de la Unión Europea a lo largo del tiempo y específicamente durante el año 2023.
Este algoritmo generará 16 gráficos de los cuales solamente se seleccionarán algunos para analizarlos en la memoria de titulo. 

2. descargar_datos3.0.py
Este script contiene un algoritmo más eficiente para descargar datos de Google Trends de forma semanal entre los años 2010 y 2023. Los datos descargados se almacenan en la carpeta "data in". Este algoritmo incluye la traducción para cada país de la palabra desánimo ya que esta no se encuentra en forma genérica para Pythrends.

3. Carpeta data in
Contiene los datos en formato CSV descargados de Google Trends, organizados por años entre 2010 y 2023. Actualizados con la palabra "desámimo" traducida para cada país en su idioma local

4. Carpeta data out
Contiene los datos consolidados y procesados, listos para ser analizados en el notebook visual.ipynb.


ARCHIVOS DESCONTINUADOS

-descargar_datos2.0.py
-visual.ypnb

