# Usar una imagen base de Python 3.10
FROM python:3.10

# Instalar UV
RUN pip install uv

# Establecer el directorio de trabajo
WORKDIR /notebooks

# Crear el entorno virtual usando UV
RUN uv venv .venv

# Copiar el archivo de configuración de UV (pyproject.toml) al contenedor
COPY pyproject.toml /notebooks/pyproject.toml

# Instalar las dependencias definidas en pyproject.toml mediante UV
RUN uv install

# Copiar archivos del proyecto
COPY Modelo_ML.ipynb /notebooks
COPY data /notebooks/data

# Añadir el entorno virtual al PATH
ENV PATH="/notebooks/.venv/bin:$PATH"

# Exponer el puerto para JupyterLab
EXPOSE 8888

# Comando de inicio de JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
