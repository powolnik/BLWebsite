#!/usr/bin/env bash
# BLACK LIGHT Collective — Build Script (Render)
set -o errexit

# --- Krok 1: Python deps ---
echo "=== [1/5] Installing Python dependencies ==="
pip install -r requirements.txt

# --- Krok 2: Frontend .env.production (ensure API URL is relative) ---
echo "=== [2/5] Setting frontend env ==="
cat > ../frontend/.env.production << 'ENV'
VITE_API_URL=/api
VITE_APP_NAME=BlackLightCollective
ENV

# --- Krok 3: Build React ---
echo "=== [3/5] Building React frontend ==="
cd ../frontend
npm install --legacy-peer-deps
npm run build
echo "React built! $(find dist -type f | wc -l) files"

# --- Krok 4: Copy build to Django ---
echo "=== [4/5] Copying React build to Django ==="
rm -rf ../backend/frontend_dist
mkdir -p ../backend/frontend_dist
cp -r dist/* ../backend/frontend_dist/
echo "Copied $(find ../backend/frontend_dist -type f | wc -l) files to frontend_dist/"
cd ../backend

# --- Krok 5: Collect static ---
echo "=== [5/5] Collecting static files ==="
python manage.py collectstatic --noinput

echo ""
echo "========================================="
echo "  BUILD COMPLETE!"
echo "========================================="
