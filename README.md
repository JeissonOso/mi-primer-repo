# Taller 2: Desarrollo de ML en Contenedores con UV, JupyterLab y FastAPI
## Grupo 5 - Clase de los martes

Este proyecto ilustra cómo:
1. Entrenar modelos de **Machine Learning** en un **Notebook de JupyterLab**.
2. Guardarlos en un **volumen de Docker** (sin “quemarlos” en la imagen).
3. Exponer dichos modelos a través de una **API de FastAPI**, que al iniciarse, lee esos archivos `.pkl`.

Con esta arquitectura, al entrenar o reentrenar un modelo en el Notebook, se genera un archivo `.pkl` que queda alojado en un **volumen**, y la API puede usarlo inmediatamente sin requerir una recompilación de imágenes.

### **Beneficios del Enfoque**
- **Modelos dinámicos y accesibles:** Los modelos `.pkl` se almacenan en un volumen, evitando que se "quemen" dentro de la imagen Docker.
- **Modularidad y separación de responsabilidades:** JupyterLab se encarga del entrenamiento y almacenamiento de modelos, mientras que la API los consume para realizar inferencias.
- **Despliegue eficiente:** La API accede siempre a la versión más reciente del modelo sin necesidad de reconstruir imágenes o reiniciar contenedores, optimizando el flujo de trabajo.

---

## Estructura del Proyecto

El proyecto se organiza en tres carpetas principales:

- **`data/`**  
  Contiene los archivos CSV usados para entrenar (por ejemplo, `penguins_size.csv` y `penguins_lter.csv`).

- **`jupyter-lab-custom/`**  
  - `Dockerfile` y `pyproject.toml`: Configuración para levantar un contenedor de **JupyterLab** con UV.
  - **`models/`**: Carpeta donde se guardan los modelos entrenados en formato `.pkl`.
  - `train_penguins.ipynb`: Notebook que entrena y guarda los modelos.

- **`api/`**  
  - `Dockerfile` y `pyproject.toml`: Configuración para la API de **FastAPI**.
  - `main.py`: Código que carga los modelos desde la carpeta `models/` y expone endpoints para realizar inferencias.

---

## Configuración de Docker Compose y Volúmenes

El archivo `docker-compose.yml` define dos servicios que interactúan mediante volúmenes compartidos:

- **Jupyter Service:**  
  Levanta un contenedor con JupyterLab para entrenar los modelos. Se monta el directorio del Notebook y la carpeta de datos para trabajar con los archivos locales.

- **API Service:**  
  Levanta un contenedor con FastAPI para exponer endpoints de inferencia. Monta el directorio de modelos generado por JupyterLab, de forma que la API pueda cargar y utilizar los modelos sin necesidad de reconstruir la imagen.

```yaml
version: "3.10"

services:
  jupyter_service:
    build:
      context: ./jupyter-lab-custom
    container_name: "jupyter_uv"
    ports:
      - "8888:8888"
    volumes:
      - ./jupyter-lab-custom:/home/jovyan/work
      - ./data:/home/jovyan/work/data
    restart: always

  api_service:
    build:
      context: ./api
    container_name: "penguin_api_uv"
    ports:
      - "8989:8000"
    volumes:
      - ./jupyter-lab-custom/models:/app/models
    restart: always


Construir y Levantar los Contenedores
Ejecuta el siguiente comando en la terminal para construir las imágenes Docker y levantar los contenedores:
docker-compose up --build
Este comando:
Construirá las imágenes Docker para JupyterLab y FastAPI.
Levantará los contenedores y mapeará los puertos correspondientes.
Asegurará que ambos contenedores se reinicien automáticamente en caso de fallo.
Una vez ejecutado el comando, los servicios estarán disponibles en:

JupyterLab: http://127.0.0.1:8888/lab
API FastAPI: http://127.0.0.1:8989/docs


Realizar Inferencias con la API
Usa el endpoint \texttt{/predict} para enviar una solicitud POST. Por ejemplo, para el modelo "Random forests", el cuerpo de la solicitud podría ser:

{
  "island": "Biscoe",
  "culmen_length_mm": 50.0,
  "culmen_depth_mm": 18.5,
  "flipper_length_mm": 200.0,
  "body_mass_g": 4000.0,
  "sex": "MALE"
}

