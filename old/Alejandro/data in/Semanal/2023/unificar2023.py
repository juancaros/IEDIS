import os
import pandas as pd
from glob import glob
import datetime

# Ruta de los archivos CSV
path = './'  # ajusta la ruta según la ubicación de tus archivos
files = glob(path + '*-*.csv')

# Mapeo de códigos de países a nombres de países
country_mapping = {
    'DE': 'Alemania',
    'AT': 'Austria',
    'BE': 'Bélgica',
    'CY': 'Chipre',
    'HR': 'Croacia',
    'SK': 'Eslovaquia',
    'SI': 'Eslovenia',
    'ES': 'España',
    'EE': 'Estonia',
    'FI': 'Finlandia',
    'FR': 'Francia',
    'GR': 'Grecia',
    'IE': 'Irlanda',
    'IT': 'Italia',
    'LV': 'Letonia',
    'LT': 'Lituania',
    'LU': 'Luxemburgo',
    'MT': 'Malta',
    'NL': 'Países Bajos',
    'PT': 'Portugal'
}

# Lista para almacenar los DataFrames
data_frames = []

# Leer cada archivo y procesarlo
for file in files:
    try:
        # Extraer la palabra clave y el código del país del nombre del archivo
        parts = file.split('/')[-1].split('-')
        palabra_clave = parts[0].replace('.\\', '')  # Eliminar el prefijo ".\\"
        codigo_google_trend = parts[1].split('.')[0]
        
        # Obtener el nombre del país correspondiente al código
        pais = country_mapping.get(codigo_google_trend, 'Desconocido')
        
        # Leer el archivo CSV con la fila de encabezado
        df_temp = pd.read_csv(file)
        
        # Verificar si el archivo tiene exactamente tres columnas
        if df_temp.shape[1] == 3:
            df_temp.columns = ['Fecha', 'Puntuación', 'isPartial']
            # Eliminar la columna 'isPartial' ya que no la necesitamos
            df_temp = df_temp.drop(columns=['isPartial'])
        else:
            print(f"Archivo {file} tiene un formato inesperado y será omitido.")
            continue
        
        # Obtener la fecha de creación del archivo
        creation_time = os.path.getctime(file)
        created_at = datetime.datetime.fromtimestamp(creation_time).strftime('%d/%m/%Y')
        
        # Añadir las columnas adicionales
        df_temp['Palabra Clave'] = palabra_clave
        df_temp['País'] = pais
        df_temp['Código Google Trend'] = codigo_google_trend
        df_temp['Created_at'] = created_at
        
        # Reorganizar las columnas
        df_temp = df_temp[['Fecha', 'Palabra Clave', 'Puntuación', 'País', 'Código Google Trend', 'Created_at']]
        
        # Añadir el DataFrame a la lista
        data_frames.append(df_temp)
    except Exception as e:
        print(f"Error procesando el archivo {file}: {e}")

# Unir todos los DataFrames en uno solo
if data_frames:
    final_df = pd.concat(data_frames, ignore_index=True)
    # Guardar el DataFrame final a un archivo CSV
    final_df.to_csv('unificado_google_trends2.csv', index=False)
    print("Archivo unificado creado con éxito.")
else:
    print("No se han encontrado archivos CSV válidos.")
