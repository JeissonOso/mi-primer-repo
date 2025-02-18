# Dockerfile para JupyterLab
FROM python:3.10

# Instalar UV
RUN pip install uv

# Establecer el directorio de trabajo
WORKDIR /notebooks

# Crear el entorno virtual usando UV
RUN uv venv .venv

# Copiar el archivo de configuración (pyproject.toml) al contenedor
COPY pyproject.toml /notebooks/pyproject.toml

# Instalar las dependencias para JupyterLab
RUN uv pip install jupyterlab pandas numpy scikit-learn joblib uvicorn

# Copiar archivos del proyecto (por ejemplo, notebooks, datos, etc.)
COPY Modelo_ML.ipynb /notebooks
COPY data /notebooks/data

# Añadir el entorno virtual al PATH
ENV PATH="/notebooks/.venv/bin:$PATH"

# Exponer el puerto para JupyterLab
EXPOSE 8888

# Comando de inicio para JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
