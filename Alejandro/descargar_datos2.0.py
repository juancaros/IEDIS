from pytrends.request import TrendReq
import os
from time import sleep
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

palabras = {
    "Ansiedad": "/m/0k_9",
    "Depresión": "/m/03f_cb",
    "Desánimo": "desánimo",
    "Psicólogo": "/m/0jgxn",
    "Psicoterapia": "/m/06796"
}
años = [str(año) for año in range(2023, 2009, -1)]

largo=len(palabras)*len(paises)*len(años)
print(largo)
contador=0
porcentaje_global=0
porcentaje_anual=0

pytrend = TrendReq()
for year in años:
    porcentaje_anual=0
    for palabra in palabras.keys():
        for codigo in paises.values():
            archivo = os.path.join(year, palabra+"-"+codigo+".csv")
            if os.path.isfile(archivo):
                print(palabra+"-"+codigo+".csv ya existe, no se generará nuevamente")
            else:
                # Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()
                pytrend.build_payload(kw_list=[palabras.get(palabra)],geo=codigo,timeframe=year+'-01-01 '+year+'-12-31')
                # Interest Over Time
                interest_over_time_df = pytrend.interest_over_time()
                interest_over_time_df.to_csv(archivo)
                print(archivo+" creado existosamente")
                sleep(1)
            porcentaje_anual+=1
            contador+=1
            porcentaje_global=100*contador/largo
            print("porcentaje anual ("+year+"): "+str(porcentaje_anual)+"%")
            print("porcentaje global: "+str(porcentaje_global)+"%")
            

