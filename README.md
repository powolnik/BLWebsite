# ⚫ BLACK LIGHT Collective

> **Kolektyw tworzący scenografie festiwalowe — dekoracje, oświetlenie, efekty specjalne na festiwalach muzyki elektronicznej.**

![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)
![React](https://img.shields.io/badge/React-19-blue?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue?logo=typescript)
![Three.js](https://img.shields.io/badge/Three.js-R3F-black?logo=three.js)
![Render](https://img.shields.io/badge/Deploy-Render-purple?logo=render)

---

## 📋 Spis treści

- [O projekcie](#-o-projekcie)
- [Architektura](#-architektura)
- [Technologie](#-technologie)
- [Funkcje](#-funkcje)
- [3D Scene Builder](#-3d-scene-builder)
- [Konfigurator 2D](#-konfigurator-2d)
- [Panel admina](#-panel-admina)
- [Sklep](#-sklep)
- [Instalacja lokalna](#-instalacja-lokalna)
- [Deployment na Render](#-deployment-na-render)
- [API Reference](#-api-reference)
- [Konta testowe](#-konta-testowe)
- [Struktura plików](#-struktura-plików)
- [Rozwój projektu](#-rozwój-projektu)

---

## 🌟 O projekcie

**BLACK LIGHT Collective** to platforma webowa dla kolektywu zajmującego się projektowaniem i budową scenografii na festiwalach muzyki elektronicznej. Strona umożliwia:

- **Prezentację portfolio** — zrealizowane projekty z galeriami zdjęć
- **Konfigurację scen 2D** — interaktywny konfigurator z modułami (UFO, lasery, LED, etc.)
- **Budowanie scen 3D** — zaawansowany builder z siatką centymetrową, detekcją kolizji i fizyką
- **Sklep online** — merch, elementy sceniczne, druki artystyczne
- **Zarządzanie zamówieniami** — pełny system od wyceny po realizację

---

## 🏗️ Architektura

```
┌─────────────────────────────────────────────────────────────┐
│                    RENDER (Free Tier)                        │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Django + Gunicorn + WhiteNoise            │  │
│  │                                                       │  │
│  │   /api/*           → Django REST Framework (DRF)      │  │
│  │   /admin/          → Django Admin Panel                │  │
│  │   /assets/*        → WhiteNoise (React build)         │  │
│  │   /*               → React SPA (catch-all)            │  │
│  │                                                       │  │
│  │   Frontend jest WBUDOWANY w Django (zero kosztów)     │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                                 │
│  ┌────────────────────────▼──────────────────────────────┐  │
│  │              PostgreSQL (Free Tier)                    │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Kluczowa decyzja:** Cały frontend (React) jest serwowany przez Django via WhiteNoise. Nie ma osobnego serwisu na statykę — **zero dodatkowych kosztów**.

---

## 🛠️ Technologie

### Backend
| Technologia | Zastosowanie |
|---|---|
| **Django 4.2** | Framework webowy |
| **Django REST Framework** | API REST |
| **SimpleJWT** | Autentykacja JWT (access + refresh tokens) |
| **WhiteNoise** | Serwowanie plików statycznych (frontend) |
| **dj-database-url** | Konfiguracja bazy z URL |
| **django-filter** | Filtrowanie API |
| **django-cors-headers** | CORS dla frontendu |
| **Gunicorn** | Serwer WSGI (produkcja) |
| **PostgreSQL** | Baza danych |

### Frontend
| Technologia | Zastosowanie |
|---|---|
| **React 19** | UI framework |
| **TypeScript 5.x** | Typowanie statyczne |
| **Vite** | Build tool (szybki HMR + bundle) |
| **React Three Fiber** | Rendering 3D (Three.js wrapper) |
| **@react-three/drei** | Helpers 3D (OrbitControls, Grid, etc.) |
| **Three.js** | Silnik 3D (WebGL) |
| **Zustand** | State management (lekki, bez boilerplate'u) |
| **React Router 7** | Routing SPA |
| **Tailwind CSS** | Styling utility-first |
| **Lucide React** | Ikony |
| **clsx** | Conditional CSS classes |

### Scene Engine (TypeScript + C++)
| Technologia | Zastosowanie |
|---|---|
| **TypeScript** | Główna implementacja silnika (działa od razu) |
| **C++ / Emscripten** | Opcjonalna kompilacja do WASM (10-20× szybszy) |
| **Octree** | Spatial indexing (szybkie zapytania o kolizje) |
| **AABB** | Axis-Aligned Bounding Box collision detection |

---

## ✨ Funkcje

### 🎨 Portfolio
- Lista projektów z filtrami (kategoria, festiwal, wyróżnione)
- Strona szczegółowa z galerią zdjęć
- Opinie klientów z ocenami
- Profil członków zespołu

### 🛸 Konfigurator 2D (istniejący)
- 21 modułów w 6 kategoriach (UFO, Las, Lasery, LED, Konstrukcje, Efekty)
- Drag & drop na canvasie 2D
- Statystyki: ⚡ moc, ⚖️ waga, 💰 cena
- Wybór szablonów sceny (Main Stage, Techno Bunker, Forest, etc.)

### 🎮 3D Scene Builder (nowy!)
- Siatka sześcienna 20m × 10m × 20m z podziałką 1cm
- Biblioteka 15 modeli 3D w 6 kategoriach
- Snap-to-grid z dokładnością centymetrową
- Detekcja kolizji AABB z Octree
- Fizyka: masa, środek ciężkości, balans, stabilność
- Eksport sceny do JSON / binarnego formatu BL3D
- Orbit camera z zoomem
- Narzędzia: przesuwanie, rotacja, skalowanie

### 🛒 Sklep
- Produkty w kategoriach (odzież, akcesoria, elementy sceniczne, druki)
- Koszyk z CRUD
- System kuponów rabatowych
- Checkout z danymi wysyłki
- Historia zamówień

### 👤 Konta użytkowników
- Rejestracja + logowanie (JWT)
- 3 role: admin, member, client
- Profil z avatarem, bio, firmą
- Adresy dostawy

---

## 🎮 3D Scene Builder

### Architektura silnika

```
┌──────────────────────────────┐
│      React Three Fiber       │  ← Rendering 3D (GPU/WebGL)
│      (SceneCanvas.tsx)       │
├──────────────────────────────┤
│      Zustand Store           │  ← State management
│  (sceneBuilderStore.ts)      │
├──────────────────────────────┤
│     SceneEngine (TS)         │  ← Logika sceny
│     - Octree                 │     Snap-to-grid, kolizje,
│     - AABB Collision         │     fizyka, serializacja
│     - Physics                │
│     - Binary Serializer      │
├──────────────────────────────┤
│     [SceneEngine (C++)]      │  ← Opcjonalny WASM (10-20× faster)
│     via Emscripten           │     Identyczny interfejs ISceneEngine
└──────────────────────────────┘
```

### Komponenty React

| Komponent | Opis |
|---|---|
| `SceneBuilder.tsx` | Strona główna — layout 3-kolumnowy |
| `ModelLibrary.tsx` | Panel lewy — biblioteka modeli z wyszukiwaniem |
| `SceneCanvas.tsx` | Centrum — canvas Three.js z OrbitControls |
| `CubicGrid.tsx` | Siatka 3D z osiami i znacznikami wysokości |
| `SceneObject3D.tsx` | Pojedynczy obiekt 3D (box + wireframe + interakcja) |
| `PropertiesPanel.tsx` | Panel prawy — narzędzia, transformacje, fizyka |

### Silnik TypeScript (`SceneEngine.ts`)

```typescript
// Główne operacje
engine.addObject(modelId, x, y, z, rx, ry, rz, sx, sy, sz, bboxW, bboxH, bboxD, weight)
engine.moveObject(id, x, y, z)        // snap-to-grid automatyczny
engine.checkCollision(id)              // AABB + Octree
engine.calculatePhysics()              // masa, CoM, balans
engine.toJSON() / engine.fromJSON()    // serializacja
engine.toBinary() / engine.fromBinary() // format BL3D
```

### Swap na WASM

Interfejs `ISceneEngine` jest identyczny dla TS i WASM. Aby przełączyć na WASM:

```typescript
// W sceneBuilderStore.ts zamień:
import { SceneEngine } from '../engine/SceneEngine';
// Na:
import { WasmSceneEngine as SceneEngine } from '../engine/WasmSceneEngine';
```

---

## ⚙️ Instalacja lokalna

### Wymagania
- Python 3.12+
- Node.js 20+
- PostgreSQL (lub SQLite na dev)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Konfiguracja (opcjonalnie)
export DJANGO_SETTINGS_MODULE=config.settings.dev

# Migracje
python manage.py makemigrations
python manage.py migrate

# Dane przykładowe
python manage.py seed_data

# Start
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install --legacy-peer-deps
npm run dev
```

Frontend będzie na `http://localhost:5173`, API na `http://localhost:8000`.

---

## 🚀 Deployment na Render

### Automatyczny (Blueprint)

1. Wrzuć kod na GitHub
2. Na Render: **New → Blueprint → Import repo**
3. `render.yaml` automatycznie skonfiguruje:
   - Serwis webowy (Python, free tier)
   - Bazę PostgreSQL (free tier)
4. Ustaw zmienną `DATABASE_URL` z **External URL** bazy (jeśli potrzeba)

### Ręczny

1. **New Web Service** → Connect repo
2. **Root Directory:** `backend`
3. **Build Command:** `bash build.sh`
4. **Start Command:** `bash start.sh`
5. **Environment Variables:**
   - `DJANGO_SETTINGS_MODULE` = `config.settings.prod`
   - `DJANGO_SECRET_KEY` = (wygeneruj)
   - `ALLOWED_HOSTS` = `.onrender.com`
   - `DATABASE_URL` = (External URL z Render PostgreSQL)

### Proces build/deploy

```
build.sh:  pip install → npm build → copy dist → collectstatic
start.sh:  makemigrations → migrate → seed_data → gunicorn
```

---

## 📡 API Reference

### Autentykacja
| Endpoint | Method | Opis |
|---|---|---|
| `/api/token/` | POST | Uzyskaj JWT (username + password) |
| `/api/token/refresh/` | POST | Odśwież access token |
| `/api/accounts/register/` | POST | Rejestracja |
| `/api/accounts/profile/` | GET/PUT | Profil użytkownika |

### Portfolio
| Endpoint | Method | Opis |
|---|---|---|
| `/api/portfolio/projects/` | GET | Lista projektów |
| `/api/portfolio/projects/{slug}/` | GET | Szczegóły projektu |
| `/api/portfolio/team/` | GET | Członkowie zespołu |
| `/api/portfolio/festivals/` | GET | Festiwale |
| `/api/portfolio/testimonials/` | GET | Opinie klientów |

### Konfigurator 2D
| Endpoint | Method | Opis |
|---|---|---|
| `/api/configurator/templates/` | GET | Szablony scen |
| `/api/configurator/categories/` | GET | Kategorie komponentów |
| `/api/configurator/components/` | GET | Lista modułów |
| `/api/configurator/orders/` | GET/POST | Zamówienia scen |

### 3D Scene Builder
| Endpoint | Method | Opis |
|---|---|---|
| `/api/scene-builder/categories/` | GET | Kategorie modeli 3D |
| `/api/scene-builder/models/` | GET | Modele 3D (GLB/GLTF) |
| `/api/scene-builder/models/upload/` | POST | Upload modelu (admin) |
| `/api/scene-builder/scenes/` | GET/POST | Zapisane sceny |
| `/api/scene-builder/scenes/{slug}/export-binary/` | GET | Eksport BL3D |

### Sklep
| Endpoint | Method | Opis |
|---|---|---|
| `/api/shop/products/` | GET | Lista produktów |
| `/api/shop/products/{slug}/` | GET | Szczegóły produktu |
| `/api/shop/cart/` | GET/POST/PUT/DELETE | Koszyk |
| `/api/shop/checkout/` | POST | Złóż zamówienie |
| `/api/shop/coupon/validate/` | POST | Waliduj kupon |
| `/api/shop/orders/` | GET | Historia zamówień |

---

## 🔑 Konta testowe

| Login | Hasło | Rola | Opis |
|---|---|---|---|
| `admin` | `admin123!` | Admin | Pełny dostęp + Django Admin |
| `kasia.led` | `member123!` | Member | Członek zespołu |
| `marek.bass` | `member123!` | Member | Członek zespołu |
| `jan.kowalski` | `client123!` | Client | Klient z zamówieniami |
| `anna.nowak` | `client123!` | Client | Klientka |
| `tomek.dj` | `client123!` | Client | Klient |

Django Admin: `/admin/` (login: `admin` / `admin123!`)

---

## 📁 Struktura plików

Szczegółowy opis w pliku `STRUCTURE.txt`.

---

## 🔮 Rozwój projektu

### Planowane
- [ ] Upload prawdziwych modeli GLB/GLTF i renderowanie w Scene Builder
- [ ] Kompilacja C++ → WASM (Emscripten) dla 10-20× wydajności
- [ ] Drag & drop obiektów na scenie 3D (TransformControls z R3F)
- [ ] Integracja płatności (Stripe / Przelewy24)
- [ ] Powiadomienia email (zamówienia, zmiany statusu)
- [ ] Zapisywanie scen do bazy i galeria publicznych scen
- [ ] System czatu / komentarzy do zamówień
- [ ] Wersja mobilna / responsywny Scene Builder

### Opcjonalne
- [ ] WebSocket do collaborative scene editing
- [ ] AR preview sceny (WebXR)
- [ ] AI-assisted scene layout suggestions

---

## 📄 Licencja

Projekt prywatny — © BLACK LIGHT Collective. Wszelkie prawa zastrzeżone.

---

**Built with 🖤 by BLACK LIGHT Collective**
