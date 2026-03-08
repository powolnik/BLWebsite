#!/usr/bin/env bash
# ==============================================
# RENDER BUILD SCRIPT
# Buduje React frontend + Django backend
# w JEDNYM serwisie (zero dodatkowych kosztów!)
# ==============================================
set -o errexit

echo "=== [1/6] Instalacja Python dependencies ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== [2/6] Instalacja Node.js + budowanie React ==="
if ! command -v node &> /dev/null; then
    echo "Node.js nie znaleziony, instaluję..."
    apt-get update && apt-get install -y nodejs npm
fi
node --version
npm --version

cd ../frontend
npm install
# API na tej samej domenie — relative URLs (/api/...)
VITE_API_URL="" npm run build
echo "React zbudowany!"

echo "=== [3/6] Kopiowanie React builda do Django ==="
rm -rf ../backend/frontend_dist
cp -r dist ../backend/frontend_dist
echo "Skopiowano $(find ../backend/frontend_dist -type f | wc -l) plików"

cd ../backend

echo "=== [4/6] Collect static files ==="
python manage.py collectstatic --noinput

echo "=== [5/6] Generowanie migracji ==="
python manage.py makemigrations accounts portfolio configurator shop notifications --noinput

echo "=== [6/6] Database migrations ==="
python manage.py migrate --noinput

echo "=== ✅ Build zakończony pomyślnie! ==="
