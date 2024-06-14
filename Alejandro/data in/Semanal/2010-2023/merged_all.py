import os
import pandas as pd
from glob import glob

# Ruta de la carpeta con los archivos CSV
path = './'  # ajusta la ruta según la ubicación de tus archivos
files = glob(os.path.join(path, 'merged*.csv'))

# Lista para almacenar los DataFrames
data_frames = []

# Leer cada archivo y procesarlo
for file in files:
    try:
        # Leer el archivo CSV
        df_temp = pd.read_csv(file)
        
        # Añadir el DataFrame a la lista
        data_frames.append(df_temp)
    except Exception as e:
        print(f"Error procesando el archivo {file}: {e}")

# Unir todos los DataFrames en uno solo
if data_frames:
    final_df = pd.concat(data_frames, ignore_index=True)
    # Guardar el DataFrame final a un archivo CSV
   # final_df.to_csv('google_trends_semanal_2010_2023.csv', index=False)
    print("Archivo unificado creado con éxito.")
else:
    print("No se han encontrado archivos CSV válidos.")
