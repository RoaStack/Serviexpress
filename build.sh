#!/usr/bin/env bash

# Exit when any command fails
set -o errexit

echo "=== 🚀 Starting build process for ServiExpress ==="

# 1. Install dependencies
echo "1️⃣ Installing dependencies..."
pip install -r requirements.txt

# 2. Apply migrations
echo "2️⃣ Applying database migrations..."
python manage.py migrate --noinput

# 3. Create superuser automatically if env vars are present
echo "3️⃣ Checking superuser creation..."
if [ -n "$SUPERUSER_USERNAME" ] && [ -n "$SUPERUSER_PASSWORD" ] && [ -n "$SUPERUSER_EMAIL" ]; then
    echo "➡️ Creating Django superuser..."
    python create_superuser.py
else
    echo "⚠️ SUPERUSER variables not set — skipping superuser creation"
fi

# 4. Collect static files for Whitenoise
echo "4️⃣ Collecting static files..."
python manage.py collectstatic --noinput

echo "✔️ Build completed successfully!"
