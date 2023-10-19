dft = data[['date','workplaces_percent_change_from_baseline']]
dft.rename(columns={'date': 'ds', 'workplaces_percent_change_from_baseline': 'y'}, inplace=True)
md = Prophet(yearly_seasonality=False, weekly_seasonality=False)
md.add_country_holidays(country_name='ES')
md.fit(dft)
future = md.make_future_dataframe(periods=365, freq='D')
forecast = md.predict(future)
#fig = md.plot_components(forecast)