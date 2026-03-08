#!/usr/bin/env bash
# ==============================================
# RENDER BUILD SCRIPT
# Buduje React frontend + Django backend
# w JEDNYM serwisie (zero dodatkowych kosztów!)
# ==============================================
set -o errexit

echo "=== [1/5] Instalacja Python dependencies ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== [2/5] Instalacja Node.js + budowanie React ==="
# Render ma Node.js, ale upewnij się
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

echo "=== [3/5] Kopiowanie React builda do Django ==="
rm -rf ../backend/frontend_dist
cp -r dist ../backend/frontend_dist
echo "Skopiowano $(find ../backend/frontend_dist -type f | wc -l) plików"

cd ../backend

echo "=== [4/5] Collect static files ==="
python manage.py collectstatic --noinput

echo "=== [5/5] Database migrations ==="
python manage.py migrate

echo "=== ✅ Build zakończony pomyślnie! ==="
