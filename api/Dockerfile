# Dockerfile para la API de FastAPI con UV

FROM python:3.10-slim

# 1. Instalar utilidades
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 2. Instalar UV con pip
RUN pip install --no-cache-dir uv

# 3. Establecer el directorio de trabajo
WORKDIR /app

# 4. Copiar el pyproject.toml (donde definimos dependencias)
COPY pyproject.toml .

# 5. Instalar dependencias con UV
# Aquí la clave: usamos '--system' para no usar virtualenv
RUN uv pip install . --system

# 6. Copiar tu main.py a /app
COPY main.py .

# 7. Exponer el puerto 8000 dentro del contenedor
EXPOSE 8000

# 8. Comando de inicio: uv run uvicorn main:app --host 0.0.0.0 --port 8000
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


