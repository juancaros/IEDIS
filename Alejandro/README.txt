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

-Carga y preparación de datos: Carga los datos consolidados y prepara el formato adecuado para Prophet.
-Visualización de los datos originales: Grafica los datos originales de Google Trends.
-Ajuste del modelo Prophet: Ajusta un modelo Prophet a los datos.
-Predicciones: Genera y visualiza predicciones a futuro.
-Detección de anomalías: Identifica posibles anomalías en los datos.
-Cross-validation: Realiza validación cruzada para evaluar el modelo.
-Evaluación del modelo: Presenta métricas de evaluación del modelo.
-Visualización de la incertidumbre de las predicciones: Muestra la incertidumbre asociada a las predicciones.
-Descomposición de la estacionalidad y componentes de la tendencia: Descompone los datos en sus componentes principales.

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

Próximamente
Durante la tarde se agregará un archivo similar a visual.ipynb pero en formato .py, que permitirá generar y guardar imágenes de los gráficos en una carpeta específica.
