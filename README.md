# Taller 2: Desarrollo de ML en Contenedores con UV, JupyterLab y FastAPI  
**Grupo 5 - Clase de los martes**

---

## Descripción

Este proyecto integra un Notebook en JupyterLab para entrenar modelos de Machine Learning y una API en FastAPI para realizar predicciones utilizando dichos modelos. Se utiliza Docker para contener ambos entornos y se gestionan las dependencias mediante UV. Además, se comparte un volumen entre los contenedores para que los modelos entrenados en JupyterLab estén automáticamente disponibles para la API.

---

## Arquitectura del Proyecto

El desarrollo se compone de dos servicios principales definidos en el archivo `docker-compose.yml`:

- **JupyterLab**  
  - Permite entrenar modelos de ML.
  - Guarda los modelos entrenados en un volumen compartido denominado `shared-models` (montado en `/models`).

- **FastAPI**  
  - Carga automáticamente los modelos desde el volumen compartido (montado en `/app/models`).
  - Expone endpoints para listar los modelos disponibles, realizar predicciones y recargar los modelos si se modifican.

Los volúmenes compartidos definidos son:

- **shared-models:**  
  Utilizado para almacenar y compartir los modelos (`.pkl`) entre JupyterLab y FastAPI.
  
- **shared-data:**  
  (Opcional) Para compartir datos entre los contenedores.

---

## Automatización del Proceso

1. **Creación del Entorno Virtual con UV:**  
   Cada contenedor crea y activa un entorno virtual usando UV, instalando las dependencias definidas en el archivo `pyproject.toml`. Esto garantiza que tanto JupyterLab como FastAPI operen en un entorno controlado y consistente.

2. **Carga Automática de Modelos en FastAPI:**  
   Al iniciar la API, se ejecuta el evento `startup` que llama a la función `load_models()`. Esta función:
   - Verifica la existencia del directorio `/app/models`.
   - Recorre y carga todos los archivos `.pkl` del directorio, almacenándolos en una variable global.
   
   De esta manera, los modelos entrenados y guardados desde JupyterLab quedan disponibles automáticamente para ser utilizados en las predicciones de la API.

3. **Actualización Dinámica de Modelos:**  
   Si se agregan o eliminan modelos en el volumen compartido, se puede invocar el endpoint `/refresh` para recargar los modelos en la API sin necesidad de reiniciar el contenedor.

---

## Construir y Levantar los Contenedores

Ejecuta el siguiente comando en la terminal para construir las imágenes Docker y levantar los contenedores:

```bash
docker-compose up --build

