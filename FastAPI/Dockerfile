# Dockerfile para FastAPI
FROM python:3.10

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar UV
RUN pip install uv

# Crear el entorno virtual usando UV
RUN uv venv .venv

# Copiar el archivo de configuración (pyproject.toml) al contenedor
COPY pyproject.toml /app/pyproject.toml

# Instalar las dependencias para FastAPI
RUN uv pip install fastapi pydantic joblib pandas scikit-learn uvicorn

# Copiar todos los archivos del proyecto al contenedor
COPY . /app

# Añadir el entorno virtual al PATH
ENV PATH="/app/.venv/bin:$PATH"

# Exponer el puerto que usará la API
EXPOSE 8989

# Comando para iniciar la aplicación FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8989", "--reload"]
