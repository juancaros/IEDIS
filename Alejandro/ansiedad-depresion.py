import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar los datos desde el archivo CSV
file_path = 'data out/google_trends_semanal_2010_2023.csv'
data = pd.read_csv(file_path)

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

# Grupos geográficos de países
grupos = {
    "Grupo 1": ["Alemania", "Austria", "Bélgica", "Países Bajos", "Luxemburgo"],
    "Grupo 2": ["España", "Francia", "Italia", "Portugal", "Grecia"],
    "Grupo 3": ["Finlandia", "Irlanda", "Malta", "Chipre", "Estonia"],
    "Grupo 4": ["Croacia", "Eslovaquia", "Eslovenia", "Letonia", "Lituania"]
}

# Función para graficar tendencias
def plot_trends(data, paises, keyword, year=None):
    fig, ax = plt.subplots(figsize=(14, 7))
    
    for pais in paises:
        pais_data = data[(data['País'] == pais) & (data['Palabra Clave'] == keyword)]
        
        # Filtrar por año si se especifica
        if year:
            pais_data = pais_data[pais_data['Fecha'].str.startswith(str(year))]
        
        sns.lineplot(x='Fecha', y='Puntuación', data=pais_data, label=pais, ax=ax)
    
    ax.set_title(f'Tendencias de búsqueda para "{keyword}"' + (f' en {year}' if year else ''))
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Puntuación de Búsqueda')
    ax.legend(title='País')
    plt.xticks(rotation=45)
    
    # Eliminar líneas verticales de la cuadrícula
    ax.grid(True, which='major', axis='y')
    ax.grid(False, which='major', axis='x')
    
    plt.show()

# Graficar tendencias para cada grupo y cada palabra clave (2010-2023)
for grupo, paises_grupo in grupos.items():
    print(f'Gráficos para {grupo} (2010-2023)')
    for keyword in ["Ansiedad", "Depresión"]:
        plot_trends(data, paises_grupo, keyword)

# Graficar tendencias para cada grupo y cada palabra clave (2023)
for grupo, paises_grupo in grupos.items():
    print(f'Gráficos para {grupo} (2023)')
    for keyword in ["Ansiedad", "Depresión"]:
        plot_trends(data, paises_grupo, keyword, year=2023)
