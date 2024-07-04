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

# Configurar Streamlit
st.title('Análisis de Tendencias de Búsqueda en Salud Mental en la Unión Europea (2010-2023) utilizando Google Trends y Prophet')

# Cargar los datos desde el archivo CSV
file_path = 'google_trends_semanal_2010_2023.csv'
data = pd.read_csv(file_path)

# Filtrar los datos para el país y la palabra clave seleccionados
country = st.selectbox("Seleccione un país", data['País'].unique())
keyword = st.selectbox("Seleccione una palabra clave", data['Palabra Clave'].unique())

# Obtener el código del país y su nombre en inglés
country_code = country_codes.get(country)
country_h = pycountry.countries.get(alpha_2=country_code).name

# Obtener los días festivos del país seleccionado
country_data = data[(data['País'] == country) & (data['Palabra Clave'] == keyword)].copy()
country_data['Fecha'] = pd.to_datetime(country_data['Fecha'])
country_holidays = getattr(holidays, country_h)(years=range(2010, 2025))

# Crear un DataFrame de los días festivos
holidays_df = pd.DataFrame(list(country_holidays.items()), columns=['ds', 'holiday'])
holidays_df['ds'] = pd.to_datetime(holidays_df['ds'])  # Asegurarse de que la columna 'ds' sea de tipo datetime

# Mostrar los días festivos para 2024
st.subheader(f'Días festivos en {country} para 2023')
holidays_2024 = holidays_df[holidays_df['ds'].dt.year == 2023]
st.write(holidays_2024)

# Función para preparar y ajustar el modelo Prophet
def fit_prophet(df, fourier_order=10):
    df = df.rename(columns={'Fecha': 'ds', 'Puntuación': 'y'})
    df['cap'] = 100
    df['floor'] = 0
    train = df[df['ds'] < '2023-01-01']
    test = df[df['ds'] >= '2023-01-01']
    model = Prophet(growth='logistic', 
                    weekly_seasonality=True, 
                    yearly_seasonality=False, 
                    holidays=holidays_df)
    model.add_seasonality(name='Anual', period=365.25, fourier_order=fourier_order)
    model.fit(train)
    future = model.make_future_dataframe(periods=52, freq='W')
    future['cap'] = 100
    future['floor'] = 0
    forecast = model.predict(future)
    return model, forecast, test

# Función para evaluar el modelo
def evaluate_model(forecast, test):
    forecast_test = forecast[forecast['ds'].isin(test['ds'])].copy()
    test = test[test['ds'].isin(forecast_test['ds'])].copy()
    mae = mean_absolute_error(test['y'], forecast_test['yhat'])
    rmse = np.sqrt(mean_squared_error(test['y'], forecast_test['yhat']))
    return mae, rmse

# Función para graficar las predicciones
def plot_forecast(model, forecast, test, keyword):
    fig, ax = plt.subplots(figsize=(10, 6))
    model.plot(forecast, ax=ax)
    for holiday in holidays_df['ds']:
        ax.axvline(x=holiday, color='red', linestyle='--', linewidth=0.8)
    ax.set_title(f'Pronóstico para {keyword} en {country}')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Puntuación de búsqueda')
    st.pyplot(fig)
    ##
    st.subheader("Componentes de la Tendencia")
    fig2 = model.plot_components(forecast)
    st.pyplot(fig2)

    forecast_test = forecast[forecast['ds'].isin(test['ds'])]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(test['ds'], test['y'], 'r.', label='Actual')
    ax.plot(forecast_test['ds'], forecast_test['yhat'], 'b-', label='Pronóstico')
    ax.fill_between(forecast_test['ds'], forecast_test['yhat_lower'], forecast_test['yhat_upper'], color='blue', alpha=0.2)
    ax.set_title(f'Pronóstico vs datos actuales para {keyword} en {country}')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Nivel de Búsqueda')
    ax.legend()
    st.pyplot(fig)

    forecast_2023 = forecast[forecast['ds'].dt.year == 2023]
    test_2023 = test[test['ds'].dt.year == 2023]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(test_2023['ds'], test_2023['y'], 'r.', label='Actual')
    ax.plot(forecast_2023['ds'], forecast_2023['yhat'], 'b-', label='Pronóstico')
    ax.fill_between(forecast_2023['ds'], forecast_2023['yhat_lower'], forecast_2023['yhat_upper'], color='blue', alpha=0.2)
    for holiday in holidays_df['ds']:
        if holiday.year == 2023:
            ax.axvline(x=holiday, color='red', linestyle='--', linewidth=0.8)
    ax.set_title(f'Pronóstico para {keyword} en {country} en 2023, festivos incluidos.')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Puntuación de búsqueda')
    ax.legend()
    st.pyplot(fig)

# Buscar el mejor orden de Fourier
best_mae = float('inf')
best_rmse = float('inf')
best_fourier_order = 0
best_model = None
best_forecast = None
best_test = None

for order in range(5, 21, 5):
    model, forecast, test = fit_prophet(country_data[['Fecha', 'Puntuación']], fourier_order=order)
    mae, rmse = evaluate_model(forecast, test)

    if mae < best_mae:
        best_mae = mae
        best_rmse = rmse
        best_fourier_order = order
        best_model = model
        best_forecast = forecast
        best_test = test

# Mostrar los mejores resultados

st.markdown(f"""
<div style="background-color: #f0f0f5; padding: 20px; border-radius: 10px;">
    <h3 style="text-align: center;">Análisis del Pronóstico</h3>
    <p style="text-align: center;"><b>Mejor Orden de Fourier:</b> {best_fourier_order}</p>
    <p style="text-align: center;"><b>Mejor MAE (Error Absoluto Medio):</b> {best_mae:.2f}</p> 
    <p style="text-align: center;"><b>Mejor RMSE (Raíz del Error Cuadrático Medio):</b> {best_rmse:.2f}</p>
</div>
""", unsafe_allow_html=True)

# Graficar las predicciones usando el mejor modelo
plot_forecast(best_model, best_forecast, best_test, keyword)




