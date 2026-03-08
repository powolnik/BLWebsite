#!/usr/bin/env bash
# ==============================================
# RENDER BUILD SCRIPT
# Buduje React frontend + Django backend
# w JEDNYM serwisie (zero dodatkowych kosztów!)
# ==============================================
set -o errexit

echo "=== [1/7] Instalacja Python dependencies ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== [2/7] Instalacja Node.js + budowanie React ==="
if ! command -v node &> /dev/null; then
    echo "Node.js nie znaleziony, instaluję..."
    apt-get update && apt-get install -y nodejs npm
fi
node --version
npm --version

cd ../frontend
npm install
VITE_API_URL="" npm run build
echo "React zbudowany!"

echo "=== [3/7] Kopiowanie React builda do Django ==="
rm -rf ../backend/frontend_dist
cp -r dist ../backend/frontend_dist
echo "Skopiowano $(find ../backend/frontend_dist -type f | wc -l) plików"

cd ../backend

echo "=== [4/7] Collect static files ==="
python manage.py collectstatic --noinput

echo "=== [5/7] Generowanie migracji ==="
python manage.py makemigrations accounts portfolio configurator shop notifications --noinput

echo "=== [6/7] Database migrations ==="
python manage.py migrate --noinput

echo "=== [7/7] Ładowanie przykładowych danych ==="
python manage.py seed_data
echo "Dane załadowane!"

echo "=== ✅ Build zakończony pomyślnie! ==="
