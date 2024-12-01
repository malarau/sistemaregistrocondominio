# Establecer la imagen base para la aplicación
FROM python:3.11-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt /app/requirements.txt

# Instalar las dependencias de Python
RUN pip install psycopg2-binary
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar todo el código fuente de la aplicación al contenedor
COPY app /app

# Establecer el comando para ejecutar la aplicación Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
