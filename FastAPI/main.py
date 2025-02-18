# main.py

# ------------------------------------------------------------------------------
# Importaciones necesarias
# ------------------------------------------------------------------------------
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import uvicorn
import pandas as pd
from typing import Optional

# ------------------------------------------------------------------------------
# 1. Creación de la app
# ------------------------------------------------------------------------------
app = FastAPI(
    title="Penguin Classifier API",
    description="API que permite cargar modelos de ML para clasificar pingüinos.",
    version="2.0"
)

# ------------------------------------------------------------------------------
# 2. Definimos el esquema de datos de entrada con Pydantic 
# ------------------------------------------------------------------------------
class PenguinFeatures(BaseModel):
    island: str
    culmen_length_mm: float
    culmen_depth_mm: float
    flipper_length_mm: float
    body_mass_g: float
    sex: str

# ------------------------------------------------------------------------------
# 3. Variable global para almacenar los modelos
# ------------------------------------------------------------------------------
models = {}

# ------------------------------------------------------------------------------
# 4. Función para cargar modelos desde el directorio compartido
# ------------------------------------------------------------------------------
def load_models():
    global models
    model_directory = "/app/models"  # Ruta donde los modelos .pkl están montados

    if not os.path.exists(model_directory):
        print(f"Directorio de modelos no encontrado: {model_directory}")
        return

    # Reiniciamos el diccionario de modelos para recargarlo completamente
    models.clear()

    # Buscar y cargar todos los archivos .pkl en el directorio
    for model_file in os.listdir(model_directory):
        if model_file.endswith(".pkl"):
            model_path = os.path.join(model_directory, model_file)
            model_name = model_file.replace(".pkl", "")  # Nombre del modelo sin extensión
            print(f"Cargando modelo: {model_name} desde {model_path}")
            try:
                models[model_name] = joblib.load(model_path)
            except Exception as e:
                print(f"Error al cargar el modelo {model_name}: {e}")

# ------------------------------------------------------------------------------
# 5. Evento de inicio (startup) para cargar los modelos en memoria
# ------------------------------------------------------------------------------
@app.on_event("startup")
def startup_event():
    load_models()

# ------------------------------------------------------------------------------
# 6. Endpoint para recargar los modelos (opcional)
# ------------------------------------------------------------------------------
@app.post("/refresh")
def refresh_models():
    load_models()
    return {"message": "Modelos recargados", "available_models": list(models.keys())}

# ------------------------------------------------------------------------------
# 7. Endpoint raíz ("/") para bienvenida
# ------------------------------------------------------------------------------
@app.get("/")
def read_root():
    return {
        "message": "¡Bienvenido a la Penguin Classifier API!",
        "docs": "Visita /docs para la documentación interactiva.",
        "models_endpoint": "Visita /models para ver los modelos disponibles."
    }

# ------------------------------------------------------------------------------
# 8. Endpoint para listar los modelos disponibles ("/models")
# ------------------------------------------------------------------------------
@app.get("/models")
def list_models():
    return {"available_models": list(models.keys())}

# ------------------------------------------------------------------------------
# 9. Endpoint de predicción ("/predict")
# ------------------------------------------------------------------------------
@app.post("/predict")
def predict_species(data: PenguinFeatures, model_name: str):
    # Verificar que el modelo solicitado está disponible
    if model_name not in models:
        raise HTTPException(
            status_code=404,
            detail={
                "error": f"El modelo '{model_name}' no está disponible.",
                "available_models": list(models.keys())
            }
        )

    chosen_model = models[model_name]

    # Convertir la data de entrada en un DataFrame
    input_df = pd.DataFrame([{
        "island": data.island,
        "culmen_length_mm": data.culmen_length_mm,
        "culmen_depth_mm": data.culmen_depth_mm,
        "flipper_length_mm": data.flipper_length_mm,
        "body_mass_g": data.body_mass_g,
        "sex": data.sex
    }])

    # Realizar la predicción
    try:
        prediction = chosen_model.predict(input_df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error durante la predicción: {e}")

    # Retornar la predicción
    return {
        "model_used": model_name,
        "prediction": prediction[0]  # Asumimos que la predicción es un único valor
    }

# ------------------------------------------------------------------------------
# 10. Arranque de la aplicación (para ejecutar directamente con Python)
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8989, reload=True)
