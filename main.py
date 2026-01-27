import requests
import json
from fastapi import FastAPI


# ETAPA 1: Elección y consulta de los datos
# Descargar y leer el archivo JSON
response = requests.get("https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json")
data = response.json()

# Análisis descriptivo breve
print(f"Número de películas registradas: {len(data)}")

print("\nPropiedades de cada película:")
for key, value in data[36200].items():
    print(f"- {key} {type(value)}")

print("\nEjemplo:")
for value in data[36200].values():
    print(f"- {value}")


# ETAPA 2: Desarrollar el servidor API
app = FastAPI(title="American movies")

# GET
@app.get("/movies/search")
def buscar_pelicula(title: str = "", year: int | None = None):
    results = list()
    # Filtro por título
    for movie in movies:
        if title.lower() in movie["title"].lower():
            results.append(movie)
    # Filtro por año
    if year is not None:
        for movie in results[:]: # recorremos copia de la lista
            if movie["year"] != year:
                results.remove(movie)
    # Limitamos resultados
    return results[:10]

# POST
@app.post("/movies")
def agregar_pelicula(movie: dict):
    movies.append(movie)
    return {"mensaje": "Película agregada."}

# PUT
@app.put("/movies")
def actualizar_pelicula(title: str, year: int, new_data: dict):
    # Buscar película
    for movie in movies:
        if movie["title"].lower() == title.lower() and movie["year"] == year:
            # Actualizar solo los campos pasados como parámetro
            for key, value in new_data.items():
                movie[key] = value
            return {"mensaje": "Película actualizada.", "pelicula": m}
    # Si no encuentra la película
    return {"error": "Película no encontrada"}

# DELETE
@app.delete("/movies")
def eliminar_pelicula(title: str, year: int):
    # Buscar película
    for movie in movies[:]: # recorremos copia de la lista
        if movie["title"].lower() == title.lower() and movie["year"] == year:
            movies.remove(movie)
            return {"mensaje": "Película eliminada."}
    # Si no encuentra la película
    return {"error": "Película no encontrada"}