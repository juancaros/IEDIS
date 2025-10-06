import os
from datetime import datetime
import time
from pytrends.request import TrendReq
timeframe = '2010-01-01 2024-05-18'


from datetime import datetime
translations = {
    'Ansiedad': {
        'DE': 'Angst',
        'AT': 'Angst',
        'BE': 'Angst',
        'CY': 'Άγχος',
        'HR': 'Tjeskoba',
        'SK': 'Úzkosť',
        'SI': 'Tesnoba',
        'ES': 'Ansiedad',
        'EE': 'Ärevus',
        'FI': 'Ahdistus',
        'FR': 'Anxiété',
        'GR': 'Άγχος',
        'IE': 'Anxiety',
        'IT': 'Ansia',
        'LV': 'Trauksme',
        'LT': 'Nerimas',
        'LU': 'Anxiété',
        'MT': 'Ansjetà',
        'NL': 'Angst',
        'PT': 'Ansiedade'
    },
    'Depresión': {
        'DE': 'Depression',
        'AT': 'Depression',
        'BE': 'Depressie',
        'CY': 'Κατάθλιψη',
        'HR': 'Depresija',
        'SK': 'Depresia',
        'SI': 'Depresija',
        'ES': 'Depresión',
        'EE': 'Depressioon',
        'FI': 'Masennus',
        'FR': 'Dépression',
        'GR': 'Κατάθλιψη',
        'IE': 'Depression',
        'IT': 'Depressione',
        'LV': 'Depresija',
        'LT': 'Depresija',
        'LU': 'Dépression',
        'MT': 'Depressjoni',
        'NL': 'Depressie',
        'PT': 'Depressão'
    },
    'Desánimo': {
        'DE': 'Entmutigung',
        'AT': 'Entmutigung',
        'BE': 'Ontmoediging',
        'CY': 'Αποθάρρυνση',
        'HR': 'Malodušnost',
        'SK': 'Malomyseľnosť',
        'SI': 'Malodušnost',
        'ES': 'Desánimo',
        'EE': 'Väsimus',
        'FI': 'Lannistuminen',
        'FR': 'Découragement',
        'GR': 'Αποθάρρυνση',
        'IE': 'Discouragement',
        'IT': 'Scoraggiamento',
        'LV': 'Skaidrība',
        'LT': 'Nusivylimas',
        'LU': 'Découragement',
        'MT': 'Skoraġġiment',
        'NL': 'Ontmoediging',
        'PT': 'Desânimo'
    },
    'Psicólogo': {
        'DE': 'Psychologe',
        'AT': 'Psychologe',
        'BE': 'Psycholoog',
        'CY': 'Ψυχολόγος',
        'HR': 'Psiholog',
        'SK': 'Psychológ',
        'SI': 'Psiholog',
        'ES': 'Psicólogo',
        'EE': 'Psühholoog',
        'FI': 'Psykologi',
        'FR': 'Psychologue',
        'GR': 'Ψυχολόγος',
        'IE': 'Psychologist',
        'IT': 'Psicologo',
        'LV': 'Psihologs',
        'LT': 'Psichologas',
        'LU': 'Psychologue',
        'MT': 'Psikologu',
        'NL': 'Psycholoog',
        'PT': 'Psicólogo'
    },
    'Psicoterapia': {
        'DE': 'Psychotherapie',
        'AT': 'Psychotherapie',
        'BE': 'Psychotherapie',
        'CY': 'Ψυχοθεραπεία',
        'HR': 'Psihoterapija',
        'SK': 'Psychoterapia',
        'SI': 'Psihoterapija',
        'ES': 'Psicoterapia',
        'EE': 'Psühhoteraapia',
        'FI': 'Psykoterapia',
        'FR': 'Psychothérapie',
        'GR': 'Ψυχοθεραπεία',
        'IE': 'Psychotherapy',
        'IT': 'Psicoterapia',
        'LV': 'Psihoterapija',
        'LT': 'Psichoterapija',
        'LU': 'Psychothérapie',
        'MT': 'Psikoterapija',
        'NL': 'Psychotherapie',
        'PT': 'Psicoterapia'
    }
}

def translate_term(term, country_code):
    if term in translations and country_code in translations[term]:
        return translations[term][country_code]
    else:
        raise ValueError(f'Traducción no encontrada para el término "{term}" y el código de país "{country_code}"')


def descargar_datos_google_trends(keyword, timeframe, geo):
    """
    Descarga datos de Google Trends para una palabra clave y los guarda en un archivo CSV.
    
    Parámetros:
    keyword (str): Palabra clave para la consulta.
    timeframe (str): Intervalo de tiempo para la consulta.
    geo (str): Código geográfico para la consulta.
    """
    # Definir la carpeta de destino
    folder = 'datos/data in/'

    # Crear la carpeta si no existe
    os.makedirs(folder, exist_ok=True)

    # Generar el nombre del archivo en el formato "PalabraClave-CodigoPais.csv"
    filename = f"{keyword}-{geo}.csv"
    file_path = os.path.join(folder, filename)

    # Verificar si el archivo ya existe
    if os.path.exists(file_path):
        print(f"El archivo {file_path} ya existe y no se ha descargado nuevamente.")
        return

    # Iniciar sesión en Google Trends
    pytrend = TrendReq()

    # traducir palabra clave
    keyword_translated= translate_term(keyword, geo)
    # Construir el payload con los parámetros
    pytrend.build_payload(kw_list=[keyword_translated], timeframe=timeframe, geo=geo)

    # Obtener datos de interés en el tiempo
    data = pytrend.interest_over_time()

    # Eliminar la columna 'isPartial' si está presente
    if 'isPartial' in data.columns:
        data = data.drop(columns='isPartial')

    # Agregar la columna 'created_at' con la fecha actual
    created_at = datetime.now().strftime('%Y-%m-%d')
    data['created_at'] = created_at

    # Guardar el DataFrame en un archivo CSV dentro de la carpeta especificada
    data.reset_index().to_csv(file_path, index=False)

    print(f"Los datos para '{keyword}' han sido descargados y guardados en el archivo {file_path}.")



# Listas de países y sus códigos
paises = {
    "Alemania": "DE",
    "Austria": "AT",
    "Bélgica": "BE",
    "Chipre": "CY",
    "Croacia": "HR",
    "Eslovaquia": "SK",
    "Eslovenia": "SI",
    "España": "ES",
    "Estonia": "EE",
    "Finlandia": "FI",
    "Francia": "FR",
    "Grecia": "GR",
    "Irlanda": "IE",
    "Italia": "IT",
    "Letonia": "LV",
    "Lituania": "LT",
    "Luxemburgo": "LU",
    "Malta": "MT",
    "Países Bajos": "NL",
    "Portugal": "PT"
}

# Lista de palabras clave
palabras_clave = ["Ansiedad", "Depresión", "Desanimo", "Psicólogo", "Psicoterapia"]

# Crear los archivos CSV
for pais, codigo in paises.items():
    for palabra in palabras_clave:
        filename = f"{palabra}-{codigo}.csv"
        # Llama a la función que permite descargar datos de Google Trends
        descargar_datos_google_trends(palabra, timeframe, codigo)
        # Pausa de 5 minutos (300 segundos)
        time.sleep(300)

print("Archivos CSV creados exitosamente.")
