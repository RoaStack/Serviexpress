#!/usr/bin/env bash

set -o errexit

echo "=== Iniciando proceso de build ==="

echo "1. Instalando dependencias..."
pip install -r requirements.txt

echo "2. Aplicando migraciones..."
python manage.py migrate --noinput

echo "3. Verificando creación de superusuario..."
if [ -n "$SUPERUSER_PASSWORD" ]; then
    python create_superuser.py
else
    echo "⚠️ SUPERUSER_PASSWORD no configurada - omitiendo creación de superusuario"
fi

echo "4. Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "✅ Build completado exitosamente"
