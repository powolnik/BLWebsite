 


## 🏗️ Architektura

```
Backend:  Django 5.1 + DRF + PostgreSQL + Redis + Celery  
Frontend: React 19 + TypeScript + Vite + TailwindCSS 4 + Zustand + React Query
DevOps:   Docker Compose (dev) | Render + Vercel (prod)
```

## 🚀 Szybki start

### Wymagania
- Docker & Docker Compose
- Node.js 22+ (opcjonalnie, do dev bez Docker)
- Python 3.12+ (opcjonalnie)

### Uruchomienie (Docker)

```bash
# Sklonuj repo
git clone <repo-url> && cd blacklight-project

# Uruchom wszystko
docker-compose up -d

# Stwórz superusera
docker-compose exec backend python manage.py createsuperuser

# Otwórz:
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000/api/
# Admin: http://localhost:8000/admin/
```

### Uruchomienie (bez Docker)

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements/dev.txt
cp .env.example .env  # edytuj DATABASE_URL na lokalny postgres
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Frontend (w osobnym terminalu)
cd frontend
npm install
npm run dev
```

## 📁 Struktura projektu

```
blacklight-project/
├── docker-compose.yml
├── backend/
│   ├── config/              # Konfiguracja Django
│   │   └── settings/        # base / dev / prod
│   ├── apps/
│   │   ├── accounts/        # Użytkownicy, role, JWT auth
│   │   ├── portfolio/       # Projekty, zespół, festiwale
│   │   ├── configurator/    # Kreator zamówień scen
│   │   ├── shop/            # Sklep: produkty, koszyk, zamówienia
│   │   └── notifications/   # Email/SMS (Celery tasks)
│   └── requirements/
└── frontend/
    └── src/
        ├── components/      # Reużywalne komponenty
        ├── pages/           # Strony (routing)
        ├── services/        # API calls (axios)
        ├── store/           # State management (Zustand)
        ├── hooks/           # Custom hooks
        └── types/           # TypeScript interfaces
```

## 🔑 Główne funkcje

### Faza 1 — Strona + Portfolio ✅
- [x] Landing page z animacjami (Framer Motion)
- [x] Portfolio z filtrami kategorii
- [x] Strona "O nas" z zespołem
- [x] Formularz kontaktowy
- [x] Logowanie / Rejestracja (JWT)

### Faza 2 — Konfigurator Scen ✅
- [x] Wybór szablonu sceny
- [x] Picker komponentów (oświetlenie, deko, efekty)
- [x] Podsumowanie zamówienia z cenami
- [x] Status zamówień (draft → submitted → confirmed → in_production → ready → delivered)
- [x] Panel admina do zarządzania

### Faza 3 — Sklep ✅
- [x] Katalog produktów z wyszukiwaniem
- [x] Koszyk zakupowy
- [x] Checkout z adresem dostawy
- [x] Kody rabatowe
- [x] Historia zamówień

## 🛡️ Bezpieczeństwo
- JWT Authentication (SimpleJWT)
- CORS protection
- Django security middleware
- Rate limiting (django-ratelimit)
- Input validation (DRF serializers + Zod)

## 📝 API Endpoints

| Endpoint | Opis |
|---|---|
| `POST /api/token/` | Logowanie (JWT) |
| `GET /api/portfolio/projects/` | Lista projektów |
| `GET /api/configurator/templates/` | Szablony scen |
| `POST /api/configurator/orders/` | Nowe zamówienie sceny |
| `GET /api/shop/products/` | Produkty sklepu |
| `POST /api/shop/cart/` | Dodaj do koszyka |
| `POST /api/shop/checkout/` | Złóż zamówienie |

## 📄 Licencja
MIT
