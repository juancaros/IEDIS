import pandas as pd
from glob import glob

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

# Fecha de creación
created_at = '23/05/2024'

# Leer cada archivo y procesarlo
for file in files:
    # Extraer la palabra clave y el código del país del nombre del archivo
    parts = file.split('/')[-1].split('-')
    palabra_clave = parts[0].replace('.\\', '')  # Eliminar el prefijo ".\"
    codigo_google_trend = parts[1].split('.')[0]
    
    # Obtener el nombre del país correspondiente al código
    pais = country_mapping.get(codigo_google_trend, 'Desconocido')
    
    # Leer el archivo CSV
    df = pd.read_csv(file, names=['Fecha', 'Puntuación'])
    
    # Añadir las columnas adicionales
    df['Palabra Clave'] = palabra_clave
    df['País'] = pais
    df['Código Google Trend'] = codigo_google_trend
    df['Created_at'] = created_at
    
    # Reorganizar las columnas
    df = df[['Fecha', 'Palabra Clave', 'Puntuación', 'País', 'Código Google Trend', 'Created_at']]
    
    # Añadir el DataFrame a la lista
    data_frames.append(df)

# Unir todos los DataFrames en uno solo
final_df = pd.concat(data_frames, ignore_index=True)

# Guardar el DataFrame final a un archivo CSV
final_df.to_csv('unificado_google_trends2.csv', index=False)

print("Archivo unificado creado con éxito.")
