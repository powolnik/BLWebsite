#!/usr/bin/env bash
set -o errexit

echo "=== [1/4] Instalacja Python dependencies ==="
pip install -r requirements.txt

echo "=== [2/4] Instalacja Node.js + budowanie React ==="
cd ../frontend
npm install
npm run build
echo "React zbudowan!"

echo "=== [3/4] Kopiowanie React builda do Django ==="
rm -rf ../backend/frontend_dist
mkdir -p ../backend/frontend_dist
cp -r dist/* ../backend/frontend_dist/
echo "Skopiowano $(find ../backend/frontend_dist -type f | wc -l) plików"
cd ../backend

echo "=== [4/4] Collect static files ==="
python manage.py collectstatic --noinput

echo ""
echo "========================================="
echo "  BUILD COMPLETE!"
echo "  Migrations will run on startup."
echo "========================================="
