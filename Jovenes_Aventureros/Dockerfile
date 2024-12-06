# Usa una imagen base oficial de Python
FROM python:3.12.4

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt /app/

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código del proyecto al contenedor
COPY . /app/

# Expone el puerto en el que Django servirá la aplicación (por defecto 8000)
EXPOSE 8000

# Comando por defecto para ejecutar el servidor de desarrollo de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]