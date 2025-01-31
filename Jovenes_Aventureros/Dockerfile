# Usa una imagen base de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto donde correrá la app
EXPOSE 8000

# Define el volumen para la base de datos
VOLUME ["/app/db"]

# Comando por defecto para iniciar el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]