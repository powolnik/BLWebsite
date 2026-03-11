#!/usr/bin/env bash
# =============================================================================
# BLACK LIGHT Collective — Build Script
# Skrypt budowania projektu (używany na platformie Render / CI/CD).
# Kolejność: Python deps → React build → kopiowanie builda → collectstatic.
# =============================================================================
set -o errexit  # Przerwij przy pierwszym błędzie

# --- Krok 1: Instalacja zależności Python ---
echo "=== [1/4] Instalacja Python dependencies ==="
pip install -r requirements.txt

# --- Krok 2: Budowanie frontendu React (Vite) ---
echo "=== [2/4] Instalacja Node.js + budowanie React ==="
cd ../frontend
npm install --legacy-peer-deps   # --legacy-peer-deps dla kompatybilności zależności
npm run build
echo "React zbudowany!"

# --- Krok 3: Kopiowanie builda React do Django ---
# WhiteNoise serwuje te pliki bezpośrednio z frontend_dist/
echo "=== [3/4] Kopiowanie React builda do Django ==="
rm -rf ../backend/frontend_dist
mkdir -p ../backend/frontend_dist
cp -r dist/* ../backend/frontend_dist/
echo "Skopiowano $(find ../backend/frontend_dist -type f | wc -l) plików"
cd ../backend

# --- Krok 4: Zebranie plików statycznych Django ---
echo "=== [4/4] Collect static files ==="
python manage.py collectstatic --noinput

echo ""
echo "========================================="
echo "  BUILD COMPLETE!"
echo "  Migrations will run on startup."
echo "========================================="
