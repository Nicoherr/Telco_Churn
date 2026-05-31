# Imagen base Python liviana
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto
COPY . .

# Crear carpetas necesarias para datos y logs
RUN mkdir -p IA_Proyecto/data IA_Proyecto/logs

# Ejecutar el pipeline al iniciar el contenedor
CMD ["python", "pipeline.py"]