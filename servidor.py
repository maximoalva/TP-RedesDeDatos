import json
import os
import requests
from fastapi import FastAPI, HTTPException, status, Request, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from collections import deque
from datetime import datetime, timedelta, timezone
from typing import Deque, Dict


# ETAPA 4: Configuraciones de seguridad
# Autenticación Basic
security = HTTPBasic()
USERNAME = "admin"
PASSWORD = "1234"

def verificar_credenciales(credenciales: HTTPBasicCredentials = Depends(security)) -> str:
    """
    Valida las credenciales enviadas por el cliente.

    - Lanza HTTP 401 si usuario/contraseña no son correctos.
    """
    if credenciales.username != USERNAME or credenciales.password != PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Basic"}
        )
    return credenciales.username # Devuelve el nombre del usuario autenticado


# ETAPA 1: Elección y consulta de los datos
# Si existe el archivo JSON, cargarlo
if os.path.exists('movies.json'):
    with open('movies.json', 'r', encoding='utf-8') as archivo:
        movies = json.load(archivo)
# Sino, descargarlo
else:
    response = requests.get('https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json')
    movies = response.json()
    with open('movies.json', 'w', encoding='utf-8') as archivo:
        json.dump(movies, archivo, ensure_ascii=False, indent=2)
        

# Función para guardar cambios en el JSON       
def guardar_datos():
    """
    Escribe en disco los cambios realizados sobre los datos almacenados en memoria.
    """
    with open('movies.json', 'w', encoding='utf-8') as archivo:
        json.dump(movies, archivo, ensure_ascii=False, indent=2)


# ETAPA 2: Desarrollar el servidor API
app = FastAPI(title="American movies")


# Limitación de solicitudes
VENTANA = timedelta(seconds=1)
MAX_PETICIONES = 10

cubos_ip: Dict[str, Deque[datetime]] = {}

@app.middleware("http")
async def limitador(request: Request, call_next):
    ip = request.client.host
    ahora = datetime.now(timezone.utc)
    cubo = cubos_ip.setdefault(ip, deque())
    
    # Eliminar timestamps fuera de la ventana
    while cubo and (ahora - cubo[0]) > VENTANA:
        cubo.popleft()

    if len(cubo) >= MAX_PETICIONES:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Demasiadas solicitudes: límite 10 req/s",
        )

    cubo.append(ahora)
    return await call_next(request)


# GET
@app.get("/movies/search")
def buscar_pelicula(title: str = "", year: int | None = None, genre: str = "", cast: str = ""):
    results = []
    
    for movie in movies:
        # Filtro por título
        if title and title.lower() not in movie["title"].lower():
            continue
        # Filtro por año
        if year is not None and movie["year"] != year:
            continue
        # Filtro por género
        if genre:
            if not any(
                genre.lower() in g.lower() for g in movie["genres"]
            ):
                continue
        # Filtro por cast
        if cast:
            if not any(
                cast.lower() in c.lower() for c in movie["cast"]
            ):
                continue
        
        results.append(movie) # Agregamos las películas que superaron todos los filtros
        
    # Limitamos resultados
    return results[:10]

# POST
@app.post("/movies")
def agregar_pelicula(movie: dict, user: str = Depends(verificar_credenciales)):
    movies.append(movie)
    guardar_datos()
    return {"mensaje": "Película agregada."}

# PUT
@app.put("/movies")
def actualizar_pelicula(title: str, year: int, new_data: dict, user: str = Depends(verificar_credenciales)):
    # Buscar película
    for movie in movies:
        if movie["title"].lower() == title.lower() and movie["year"] == year:
            # Actualizar solo los campos pasados como parámetro
            for key, value in new_data.items():
                movie[key] = value
            guardar_datos()
            return {"mensaje": "Película actualizada.", "pelicula": movie}
    # Si no encuentra la película
    return {"error": "Película no encontrada"}

# DELETE
@app.delete("/movies")
def eliminar_pelicula(title: str, year: int, user: str = Depends(verificar_credenciales)):
    # Buscar película
    for movie in movies[:]: # recorremos copia de la lista
        if movie["title"].lower() == title.lower() and movie["year"] == year:
            movies.remove(movie)
            guardar_datos()
            return {"mensaje": "Película eliminada."}
    # Si no encuentra la película
    return {"error": "Película no encontrada"}