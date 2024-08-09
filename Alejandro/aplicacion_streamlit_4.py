import streamlit as st
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import seaborn as sns
import holidays
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import pycountry

# Diccionario de códigos de países
country_codes = {
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
    "Portugal": "PT",
}
grupos = {
    "Grupo 1": ["Alemania", "Austria", "Bélgica", "Países Bajos", "Luxemburgo"],
    "Grupo 2": ["España", "Francia", "Italia", "Portugal", "Grecia"],
    "Grupo 3": ["Finlandia", "Irlanda", "Malta", "Chipre", "Estonia"],
    "Grupo 4": ["Croacia", "Eslovaquia", "Eslovenia", "Letonia", "Lituania"]
}
# Configurar Streamlit (con tema personalizado)
st.set_page_config(
    page_title="Análisis de Tendencias de Búsqueda",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

# Configurar Streamlit
st.markdown("<h1 style='font-size:30px;'>Tendencias de Búsqueda en Salud Mental (UE, 2010-2023)</h1>", unsafe_allow_html=True)

# Barra lateral para la selección de país, palabra clave y frecuencia
with st.sidebar:
    st.subheader('Seleccione los Filtros')
    country = st.selectbox("País", list(country_codes.keys()))
    keyword = st.selectbox("Palabra Clave", ["Ansiedad", "Depresión","Psicólogo", "Psicoterapia"])
    frequency = st.selectbox("Frecuencia de los Datos", ["Mensual (Relativizado a 14 años)", "Semanal (Relativizado a Anualmente)"])

# Nombres de archivo según la frecuencia
file_name_mensual = 'google_trends_mensual_2010_2023.csv'
file_name_semanal = 'google_trends_semanal_2010_2023.csv'


# Ruta del archivo CSV según la frecuencia seleccionada
frequency_s='Mensual'
if frequency == "Mensual (Relativizado a 14 años)":
    file_path = f'data out/{file_name_mensual}'
else:
    frequency_s='Semanal'
    file_path = f'data out/{file_name_semanal}'

# Cargar los datos desde el archivo CSV seleccionado
data = pd.read_csv(file_path)

# Obtener el código del país y su nombre en inglés
country_code = country_codes.get(country)
country_h = pycountry.countries.get(alpha_2=country_code).name

# Obtener los días festivos del país seleccionado
country_data = data[(data['País'] == country) & (data['Palabra Clave'] == keyword)].copy()
country_data['Fecha'] = pd.to_datetime(country_data['Fecha'])
country_holidays = getattr(holidays, country_h)(years=range(2010, 2025))

# Crear un DataFrame de los días festivos
holidays_df = pd.DataFrame(list(country_holidays.items()), columns=['ds', 'holiday'])
holidays_df['ds'] = pd.to_datetime(holidays_df['ds']) 


# Función para preparar y ajustar el modelo Prophet (sin búsqueda de fourier_order)
def fit_prophet(df):
    df = df.rename(columns={'Fecha': 'ds', 'Puntuación': 'y'})
    df['cap'] = 100
    df['floor'] = 0
    train = df[df['ds'] < '2023-01-01']
    test = df[df['ds'] >= '2023-01-01']
    model = Prophet(growth='logistic', 
                    weekly_seasonality=True, 
                    yearly_seasonality=True,  # Incluir estacionalidad anual
                    holidays=holidays_df)
   # model.add_seasonality(name='Anual', period=365.25, fourier_order=10)  # Orden de Fourier fijo
    model.fit(train)

    # Ajustar la frecuencia en función de la selección del usuario
    freq = 'MS' if frequency_s == 'Mensual' else 'W'
    periods = 12 if frequency_s == 'Mensual' else 52  # 12 meses o 52 semanas
    future = model.make_future_dataframe(periods=periods, freq=freq)

    future['cap'] = 100
    future['floor'] = 0
    forecast = model.predict(future)
    return model, forecast, test


# Función para graficar las predicciones
def plot_forecast(model, forecast, test, keyword):
    fig, ax = plt.subplots(figsize=(10, 6))
    model.plot(forecast, ax=ax)

    # Traducir las etiquetas de la leyenda al español
    handles, labels = ax.get_legend_handles_labels()
    labels = ['Datos reales', 'Pronóstico', 'Límite Inferior', 'Límite superior', 'Incertidumbre']  # Reemplaza las etiquetas originales
    ax.legend(handles, labels, loc='lower right')

    ax.set_title(f'Pronóstico para {keyword} en {country}')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Puntuación de búsqueda')
    st.pyplot(fig)

    # Gráfico de pronóstico para 2023 con festivos
    forecast_2023 = forecast[forecast['ds'].dt.year == 2023]
    test_2023 = test[test['ds'].dt.year == 2023]
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    ax4.plot(test_2023['ds'], test_2023['y'], 'r.', label='Actual')
    ax4.plot(forecast_2023['ds'], forecast_2023['yhat'], 'b-', label='Pronóstico')
    ax4.fill_between(forecast_2023['ds'], forecast_2023['yhat_lower'], forecast_2023['yhat_upper'], color='blue', alpha=0.2)
    for holiday in holidays_df['ds']:
        if holiday.year == 2023:
            ax4.axvline(x=holiday, color='red', linestyle='--', linewidth=0.8)
    ax4.set_title(f'Pronóstico para {keyword} en {country} en 2023, festivos incluidos.')
    ax4.set_xlabel('Fecha')
    ax4.set_ylabel('Puntuación de búsqueda')

    # Crear elementos para la leyenda (línea roja y área de incertidumbre)
    from matplotlib.patches import Patch
    handle_holiday = Patch(facecolor='none', edgecolor='red', linestyle='--', label='Feriados')
    handle_uncertainty = Patch(facecolor='blue', edgecolor='none', alpha=0.2, label='Incertidumbre')

    # Agregar los nuevos elementos a la leyenda
    handles, labels = ax4.get_legend_handles_labels()
    handles.extend([handle_holiday, handle_uncertainty])
    labels.extend(['Feriados', 'Incertidumbre'])

    # Mostrar la leyenda en la esquina inferior derecha
    ax4.legend(handles, labels, loc='lower right')
    
    # Mostrar la descomposición de estacionalidad
    st.subheader("Componentes de la Tendencia")
    fig2 = model.plot_components(forecast)
    st.pyplot(fig2)

    st.pyplot(fig4)

def plot_trends(data, paises, keyword, year=None):
    fig, ax = plt.subplots(figsize=(14, 7))

    for pais in paises:
        pais_data = data[(data['País'] == pais) & (data['Palabra Clave'] == keyword)]
        if year:
            pais_data = pais_data[pais_data['Fecha'].str.startswith(str(year))]

        # Convertir 'Fecha' a datetime
        pais_data['Fecha'] = pd.to_datetime(pais_data['Fecha'])

        sns.lineplot(x='Fecha', y='Puntuación', data=pais_data, label=pais, ax=ax)

    # Obtener el número del grupo a partir de la lista de países
    for numero, grupo in grupos.items():
        if set(paises).issubset(set(grupo)):
            numero_grupo = numero[6:]  # Extraer el número del nombre del grupo

    # Nuevo título con formato personalizado
    ax.set_title(f'Tendencia de Búsqueda para "{keyword}" en Grupo N°{numero_grupo} Durante {year}')

    # Obtener todas las fechas únicas en el DataFrame
    all_dates = pd.to_datetime(data['Fecha'].unique())

    # Filtrar las fechas del año especificado (corrección aquí)
    if year:
        all_dates = all_dates[all_dates.year == year]

    # Obtener el primer día de cada mes
    month_starts = all_dates.to_period('M').unique().to_timestamp()

    # Configurar las marcas del eje x cada mes
    ax.set_xticks(month_starts)
    ax.set_xticklabels(month_starts.strftime('%b %y'))  # Formato mes abreviado y año abreviado

    ax.set_xlabel('Fecha')  # Nueva etiqueta para el eje x
    ax.set_ylabel('Puntuación de Búsqueda')
    ax.legend(title='País')
    plt.xticks(rotation=45)
    ax.grid(True, which='major', axis='y')
    ax.grid(False, which='major', axis='x')
    ax.set_ylim(0, 100)

    st.pyplot(fig)  # Mostrar el gráfico en Streamlit


# Ajustar el modelo y graficar
model, forecast, test = fit_prophet(country_data[['Fecha', 'Puntuación']])
plot_forecast(model, forecast, test, keyword)
# Graficar por grupo de paises
st.header("Análisis Comparativo por Grupos de Países")  
for grupo, paises_grupo in grupos.items():
    print(f'Gráficos para {grupo} (2023)')
    plot_trends(data, paises_grupo, keyword, year=2023)
    
