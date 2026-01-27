import requests
import json

URL = "http://127.0.0.1:8000/movies"

def buscar_pelicula(title: str = "", year: int | None = None) -> None:
    params = {"title": title}
    if year:
        params["year"] = year
    response = requests.get(f"{URL}/search", params=params)
    print(json.dumps(response.json(), indent=2))

def agregar_pelicula(movie: dict) -> None:
    response = requests.post(URL, json=movie)
    print(response.json())

def actualizar_pelicula(title: str, year: int, new_data: dict) -> None:
    params = {"title": title, "year": year}
    response = requests.put(URL, params=params, json=new_data)
    print(response.json())

def eliminar_pelicula(title: str, year: int) -> None:
    params = {"title": title, "year": year}
    response = requests.delete(URL, params=params)
    print(response.json())

def main() -> None:
    while True:
        print("Cliente API American movies")
        print("1. Buscar película")
        print("2. Agregar película")
        print("3. Modificar película")
        print("4. Eliminar película")
        print("5. Salir")
        opcion = input("\nElija una opción: ")


        if opcion == "1":
            titulo = input("Ingrese título: ").strip()
            anio = input("Ingrese año (enter para omitir): ").strip()
            if anio:
                buscar_pelicula(titulo, int(anio))
            else:
                buscar_pelicula(titulo)
             

        elif opcion == "2":
            titulo = input("Ingrese título: ").strip()
            anio = int(input("Ingrese año: "))
            cast = input("Ingrese cast (separados por comas): ").strip()
            generos = input("Ingrese género/s (separados por comas): ").strip()

            movie = {
                "title": titulo,
                "year": anio,
                "cast": [c.strip() for c in cast.split(',')],
                "genres": [g.strip() for g in generos.split(',')],
                "href": None
            }

            agregar_pelicula(movie)


        elif opcion == "3":
            titulo = input("Ingrese título: ").strip()
            anio = int(input("Ingrese año: "))
            
            print("Ingrese cambios (enter para omitir): ")
            nuevo_titulo = input("Nuevo título: ").strip()
            nuevo_anio = input("Nuevo año: ").strip()
            nuevo_cast = input("Ingrese nuevo cast (separados por comas): ").strip()
            nuevos_generos = input("Ingrese nuevo/s género/s (separados por comas): ").strip()
            nuevo_href = input("Ingrese nuevo href: ").strip()
            nuevo_resumen = input("Ingrese nuevo resumen: ").strip()
            nuevo_thumbnail = input("Ingrese nuevo thumbnail: ").strip()
            nuevo_width = input("Ingrese nuevo ancho del thumbnail: ").strip()
            nuevo_height = input("Ingrese nueva altura del thumbnail: ").strip()

            cambios = {}
            if nuevo_titulo:
                cambios["title"] = nuevo_titulo
            if nuevo_anio:
                cambios["year"] = int(nuevo_anio)
            if nuevo_cast:
                cambios["cast"] = [c.strip() for c in nuevo_cast.split(',')]
            if nuevos_generos:
                cambios["genres"] = [g.strip() for g in nuevos_generos.split(',')]
            if nuevo_href:
                cambios["href"] = nuevo_href
            if nuevo_resumen:
                cambios["extract"] = nuevo_resumen
            if nuevo_thumbnail:
                cambios["thumbnail"] = nuevo_thumbnail
            if nuevo_width:
                cambios["thumbnail_width"] = int(nuevo_width)
            if nuevo_height:
                cambios["thumbnail_height"] = int(nuevo_height)

            if cambios:
                actualizar_pelicula(titulo, anio, cambios)
            else:
                print("No se ingresaron cambios.")


        elif opcion == "4":
            titulo = input("Ingrese título: ")
            anio = int(input("Ingrese año: "))
            eliminar_pelicula(titulo, anio)


        elif opcion == "5":
            break


        else:
            print("Opción no válida, intente de nuevo.\n")


main()