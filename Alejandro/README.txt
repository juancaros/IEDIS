Repositorio Alejandro

Este repositorio contiene herramientas para analizar datos de Google Trends utilizando la librería Prophet. Los datos cubren búsquedas semanales entre los años 2010 y 2023 para varios países y palabras clave relacionadas con temas de salud mental.

Contenido del repositorio
1. visual.ipynb
Este notebook contiene el análisis visual de los datos utilizando Prophet. Incluye:

-Carga y preparación de datos: Carga los datos consolidados y prepara el formato adecuado para Prophet.
-Visualización de los datos originales: Grafica los datos originales de Google Trends.
Ajuste del modelo Prophet: Ajusta un modelo Prophet a los datos.
-Predicciones: Genera y visualiza predicciones a futuro.
-Detección de anomalías: Identifica posibles anomalías en los datos.
-Cross-validation: Realiza validación cruzada para evaluar el modelo.
-Evaluación del modelo: Presenta métricas de evaluación del modelo.
-Visualización de la incertidumbre de las predicciones: Muestra la incertidumbre asociada a las predicciones.
-Descomposición de la estacionalidad y componentes de la tendencia: Descompone los datos en sus componentes principales.


2. descargar_datos2.0.py
Este script contiene un algoritmo más eficiente para descargar datos de Google Trends de forma semanal entre los años 2010 y 2023. Los datos descargados se almacenan en la carpeta "data in".

3. Carpeta data in
Contiene los datos en formato CSV descargados de Google Trends, organizados por años entre 2010 y 2023.

4. Carpeta data out
Contiene los datos consolidados y procesados, listos para ser analizados en el notebook visual.ipynb.

Próximamente
Durante la tarde se agregará un archivo similar a visual.ipynb pero en formato .py, que permitirá generar y guardar imágenes de los gráficos en una carpeta específica.