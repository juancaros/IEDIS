import os

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

# Lista de enfermedades
enfermedades = ["Ansiedad", "Depresión", "Desanimo", "Psicólogo", "Psicoterapia"]

# Crear los archivos CSV
for pais, codigo in paises.items():
    for enfermedad in enfermedades:
        filename = f"{enfermedad}-{codigo}.csv"
        # Crear un archivo vacío
        with open(filename, 'w') as file:
            pass

print("Archivos CSV creados exitosamente.")