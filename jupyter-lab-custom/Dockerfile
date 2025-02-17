####################################################
# Dockerfile para JupyterLab con UV, scikit-learn, etc.
####################################################

FROM jupyter/base-notebook:latest

# 1) Cambiamos a root para instalaciones
USER root

# 2) Instalar utilidades de compilación 
#    (curl, build-essential, gfortran, etc.)
RUN apt-get update && apt-get install -y curl build-essential gfortran && rm -rf /var/lib/apt/lists/*

# 3) Instalar uv con pip
RUN pip install --no-cache-dir uv

# 4) Definimos WORKDIR
WORKDIR /home/jovyan

# 5) Copiar pyproject.toml
COPY pyproject.toml .

# 6) Instalar dependencias con UV, en el sistema
RUN uv pip install . --system

# 7) Volver al usuario jovyan
USER ${NB_UID}

# 8) Exponemos puerto 8888
EXPOSE 8888

# 9) Iniciar JupyterLab sin token ni password
CMD ["start.sh", "jupyter", "lab", "--NotebookApp.token=''", "--NotebookApp.password=''"]




