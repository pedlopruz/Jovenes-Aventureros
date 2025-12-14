#!/bin/sh
set -e

# Esperar a que Postgres esté disponible
echo "Esperando a PostgreSQL en db:5432..."
until nc -z db 5432; do
  echo "PostgreSQL no disponible aún, reintentando..."
  sleep 1
done
echo "PostgreSQL listo."

# Ejecutar migraciones
echo "Aplicando migraciones..."
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput

# Arrancar servidor
echo "Iniciando servidor Django..."
exec python manage.py runserver 0.0.0.0:8000
