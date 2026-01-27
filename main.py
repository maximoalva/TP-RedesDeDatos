import requests
import json
from fastapi import FastAPI


#ETAPA 1: Elección y consulta de los datos
# Descargar y leer el archivo JSON
response = requests.get("https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json")
data = response.json()

# Análisis descriptivo breve
print(f"Número de películas registradas: {len(data)}")

print("\nPropiedades de cada película:")
for key in data[0].keys():
    print(f"- {key}")


# ETAPA 2: Desarrollar el servidor API
app = FastAPI()