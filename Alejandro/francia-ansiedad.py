import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import seaborn as sns
import holidays
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Cargar los datos desde el archivo CSV
file_path = 'data out/google_trends_semanal_2010_2023.csv'
data = pd.read_csv(file_path)

# Filtrar los datos para Francia y la palabra clave "Ansiedad"
country = "Francia"  # Cambiar este valor para seleccionar otro país
country_h="France" # nombre del pais en ingles para calcular feriado
keyword = "Ansiedad"
country_data = data[(data['País'] == country) & (data['Palabra Clave'] == keyword)].copy()

# Convertir la columna de fechas a tipo datetime
country_data['Fecha'] = pd.to_datetime(country_data['Fecha'])

# Obtener los días festivos del país seleccionado
country_holidays = getattr(holidays, country_h)(years=range(2010, 2024))

# Crear un DataFrame de los días festivos
holidays_df = pd.DataFrame(list(country_holidays.items()), columns=['ds', 'holiday'])

# Función para preparar y ajustar el modelo Prophet
def fit_prophet(df, fourier_order=10):
    # Renombrar columnas para que Prophet las entienda
    df = df.rename(columns={'Fecha': 'ds', 'Puntuación': 'y'})
    
    # Parámetros de crecimiento logístico
    df['cap'] = 100
    df['floor'] = 0
    
    # Dividir los datos en conjuntos de entrenamiento y prueba
    train = df[df['ds'] < '2023-01-01']
    test = df[df['ds'] >= '2023-01-01']
    
    # Crear y configurar el modelo Prophet
    model = Prophet(growth='logistic', 
                    weekly_seasonality=True, 
                    yearly_seasonality=False, 
                    holidays=holidays_df)
    
    # Añadir términos de Fourier para la estacionalidad anual con el orden especificado
    model.add_seasonality(name='yearly', period=365.25, fourier_order=fourier_order)
    
    # Ajustar el modelo con los datos de entrenamiento
    model.fit(train)
    
    # Crear un DataFrame futuro para hacer predicciones
    future = model.make_future_dataframe(periods=52, freq='W')
    future['cap'] = 100
    future['floor'] = 0
    forecast = model.predict(future)
    
    return model, forecast, test

# Función para evaluar el modelo
def evaluate_model(forecast, test):
    # Filtrar las predicciones para las fechas del conjunto de prueba
    forecast_test = forecast[forecast['ds'].isin(test['ds'])].copy()
    test = test[test['ds'].isin(forecast_test['ds'])].copy()
    # Calcular el error absoluto medio (MAE) y el error cuadrático medio (RMSE)
    mae = mean_absolute_error(test['y'], forecast_test['yhat'])
    rmse = np.sqrt(mean_squared_error(test['y'], forecast_test['yhat']))
    return mae, rmse

# Función para graficar las predicciones
def plot_forecast(model, forecast, test, keyword):
    # Crear el gráfico de las predicciones
    fig, ax = plt.subplots(figsize=(10, 6))
    model.plot(forecast, ax=ax)
    
    # Añadir líneas verticales para los días festivos en el país seleccionado
    for holiday in holidays_df['ds']:
        ax.axvline(x=holiday, color='red', linestyle='--', linewidth=0.8)
    
    ax.set_title(f'Forecast for {keyword} in {country}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Search Score')
    plt.show()
    
    # Crear el gráfico de los componentes del modelo
    fig2 = model.plot_components(forecast)
    plt.show()
    
    # Evaluar el modelo y graficar las predicciones vs los valores reales
    forecast_test = forecast[forecast['ds'].isin(test['ds'])]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(test['ds'], test['y'], 'r.', label='Actual')
    ax.plot(forecast_test['ds'], forecast_test['yhat'], 'b-', label='Forecast')
    ax.fill_between(forecast_test['ds'], forecast_test['yhat_lower'], forecast_test['yhat_upper'], color='blue', alpha=0.2)
    ax.set_title(f'Forecast vs Actual for {keyword} in {country}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Search Score')
    ax.legend()
    plt.show()
    
    # Graficar las predicciones y valores reales sólo para el año 2023
    forecast_2023 = forecast[forecast['ds'].dt.year == 2023]
    test_2023 = test[test['ds'].dt.year == 2023]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(test_2023['ds'], test_2023['y'], 'r.', label='Actual')
    ax.plot(forecast_2023['ds'], forecast_2023['yhat'], 'b-', label='Forecast')
    ax.fill_between(forecast_2023['ds'], forecast_2023['yhat_lower'], forecast_2023['yhat_upper'], color='blue', alpha=0.2)
    
    # Añadir líneas verticales para los días festivos en el país seleccionado durante 2023
    for holiday in holidays_df['ds']:
        if holiday.year == 2023:
            ax.axvline(x=holiday, color='red', linestyle='--', linewidth=0.8)
    
    ax.set_title(f'Forecast for {keyword} in {country} in 2023')
    ax.set_xlabel('Date')
    ax.set_ylabel('Search Score')
    ax.legend()
    plt.show()

# Buscar el mejor orden de Fourier
best_mae = float('inf')
best_rmse = float('inf')
best_fourier_order = 0
best_model = None
best_forecast = None
best_test = None

# Probar diferentes órdenes de Fourier (5, 10, 15, 20)
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

# Imprimir el mejor orden de Fourier y los errores correspondientes
print(f'Best Fourier Order: {best_fourier_order}')
print(f'Best MAE: {best_mae}')
print(f'Best RMSE: {best_rmse}')

# Graficar las predicciones usando el mejor modelo
plot_forecast(best_model, best_forecast, best_test, keyword)


