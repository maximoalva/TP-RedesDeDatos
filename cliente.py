import requests
import json

URL = "http://127.0.0.1:8000/movies"

def buscar_pelicula(title: str = "", year: int | None = None):
    params = {"title": title}
    if year:
        params["year"] = year
    response = requests.get(f"{URL}/search", params=params)
    print(json.dumps(response.json()))