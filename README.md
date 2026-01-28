# 📡 Comunicación API Cliente-Servidor
Redes de Datos - Tecnicatura Universitaria en Inteligencia Artificial

Facultad de Ciencias Exactas, Ingenieria y Agrimensura - Universidad Nacional de Rosario

## ⚙️ Requisitos
Se recomienda utilizar un entorno virtual e instalar las siguientes dependencias:
- requests
- fastapi
- uvicorn

### 🛠️ Instalación
```bash
# 1. Crear y activar entorno virtual (opcional pero recomendado).
python -m venv venv
source venv/bin/activate    # Linux / Mac
venv\Scripts\activate       # Windows

# 2. Actualizar pip (opcional).
python.exe -m pip install --upgrade pip

# 3. Instalar dependencias.
pip install requests fastapi uvicorn
```

## ▶️ Ejecución
### Iniciar el servidor
```bash
uvicorn servidor:app --reload
```
El servidor quedará disponible en:
```bash
http://127.0.0.1:8000
```
### Ejecutar el cliente
```bash
python cliente.py
```
Las operaciones de modificación de datos requieren autenticación HTTP Basic. Al iniciarse, el cliente solicitará usuario y contraseña.

Credenciales por defecto:

- Usuario: admin
- Contraseña: 1234

## 🧪 Datos
Los datos utilizados en este trabajo provienen de una base de datos obtenida mediante técnicas de scraping, que contiene información sobre películas estadounidenses extraídas de Wikipedia. Esta se encuentra disponible públicamente en el siguiente repositorio:

https://raw.githubusercontent.com/prust/wikipedia-movie-data/master/movies.json

## 👥 Autor
- Alva Máximo
