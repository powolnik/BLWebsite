/*******************************************************************************
 * scene_engine.h — Główny plik nagłówkowy silnika sceny 3D
 *                  Main header file for the 3D Scene Engine
 *
 * Projekt / Project : BLACK LIGHT Collective — 3D Scene Engine
 * Autor / Author    : BLACK LIGHT Collective
 * Opis / Description:
 *   Definiuje struktury danych i interfejs silnika sceny 3D skompilowanego
 *   do WebAssembly za pomocą Emscripten. Silnik obsługuje siatkę kubiczną
 *   z precyzją centymetrową, indeksowanie przestrzenne octree, detekcję
 *   kolizji AABB oraz obliczenia fizyczne (masa, środek ciężkości,
 *   równowaga, obciążenie konstrukcyjne).
 *
 *   Defines data structures and interface for a 3D scene engine compiled to
 *   WebAssembly via Emscripten. The engine supports a cubic grid with
 *   centimeter precision, octree spatial indexing, AABB collision detection,
 *   and physics calculations (weight, center of mass, balance, structural load).
 *
 * Funkcje / Features:
 *   1. Siatka kubiczna z precyzją centymetrową i przyciąganiem do siatki
 *      Cubic grid with centimeter precision & snap-to-grid
 *   2. Indeks przestrzenny octree do szybkich zapytań
 *      Octree spatial indexing for fast queries
 *   3. Detekcja kolizji AABB
 *      AABB collision detection
 *   4. Fizyka: masa, środek ciężkości, równowaga, obciążenie konstrukcyjne
 *      Physics: weight, center of mass, balance, structural load
 *   5. Binarna serializacja / deserializacja scen
 *      Binary serialization / deserialization of scenes
 ******************************************************************************/

#pragma once

#include <cstdint>   // uint32_t, uint16_t, uint8_t — fixed-width integer types
#include <cstring>   // std::memcpy — used in serialization
#include <cmath>     // std::sqrt, std::round, std::cos, std::sin, std::abs
#include <vector>    // std::vector — dynamic arrays for object lists, buffers
#include <unordered_map> // std::unordered_map — O(1) average lookup for objects by ID
#include <algorithm> // std::min, std::max — used in physics/collision
#include <memory>    // std::unique_ptr — RAII ownership of octree nodes

// ─────────────────────────────────────────────────────────────────────────────
// Primitives — Podstawowe typy geometryczne / Basic geometric types
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Vec3 — Trójwymiarowy wektor / Three-dimensional vector
 *
 * Używany wszędzie w silniku do reprezentowania pozycji, rotacji, skali,
 * wymiarów bounding-box itp. Wszystkie wartości w centymetrach lub stopniach.
 *
 * Used throughout the engine to represent positions, rotations, scales,
 * bounding-box dimensions, etc. All values in centimeters or degrees.
 *
 * Performance note: Passed by value where small (12 bytes), by const-ref
 * in hot paths. Operator overloads allow concise vector arithmetic.
 */
struct Vec3 {
    float x = 0, y = 0, z = 0;

    Vec3() = default;
    Vec3(float x, float y, float z) : x(x), y(y), z(z) {}

    /* Dodawanie wektorów / Vector addition */
    Vec3 operator+(const Vec3& o) const { return {x + o.x, y + o.y, z + o.z}; }
    /* Odejmowanie wektorów / Vector subtraction */
    Vec3 operator-(const Vec3& o) const { return {x - o.x, y - o.y, z - o.z}; }
    /* Mnożenie przez skalar / Scalar multiplication */
    Vec3 operator*(float s) const { return {x * s, y * s, z * s}; }
    /* Długość (norma euklidesowa) / Euclidean length (L2 norm) */
    float length() const { return std::sqrt(x * x + y * y + z * z); }
};

/**
 * AABB — Axis-Aligned Bounding Box / Prostokąt ograniczający wyrównany do osi
 *
 * Minimalny prostokąt (prostopadłościan) otaczający obiekt, którego krawędzie
 * są równoległe do osi układu współrzędnych. Kluczowa struktura dla szybkiej
 * detekcji kolizji — test przecięcia dwóch AABB to zaledwie 6 porównań.
 *
 * Axis-aligned bounding box: a minimal enclosing cuboid whose edges are
 * parallel to the coordinate axes. Key structure for fast collision detection —
 * intersection test of two AABBs requires only 6 comparisons (O(1)).
 */
struct AABB {
    Vec3 min, max;  // Narożniki: dolny-lewy-bliski i górny-prawy-daleki
                     // Corners: lower-left-near and upper-right-far

    AABB() = default;
    AABB(Vec3 mn, Vec3 mx) : min(mn), max(mx) {}

    /**
     * intersects — Sprawdza czy dwa AABB się przecinają
     *              Tests whether two AABBs overlap
     *
     * Algorytm / Algorithm: Separating Axis Theorem (SAT) dla AABB.
     * Dwa AABB NIE przecinają się, jeśli istnieje oś, na której ich
     * projekcje się nie pokrywają. Dla AABB wystarczy sprawdzić 3 osie (X,Y,Z).
     * Zwraca true jeśli brak osi separującej = obiekty kolidują.
     *
     * Two AABBs do NOT intersect if there exists a separating axis.
     * For axis-aligned boxes, only X, Y, Z axes need checking.
     * Returns true if no separating axis exists = objects collide.
     *
     * Złożoność / Complexity: O(1) — stałe 6 porównań / constant 6 comparisons
     */
    bool intersects(const AABB& o) const {
        return (min.x < o.max.x && max.x > o.min.x) &&
               (min.y < o.max.y && max.y > o.min.y) &&
               (min.z < o.max.z && max.z > o.min.z);
    }

    /**
     * contains — Czy punkt leży wewnątrz AABB (włącznie z krawędziami)
     *            Whether a point lies inside the AABB (inclusive boundaries)
     */
    bool contains(const Vec3& p) const {
        return p.x >= min.x && p.x <= max.x &&
               p.y >= min.y && p.y <= max.y &&
               p.z >= min.z && p.z <= max.z;
    }

    /**
     * containsAABB — Czy inny AABB mieści się w całości wewnątrz tego AABB
     *                Whether another AABB is fully contained within this one
     */
    bool containsAABB(const AABB& o) const {
        return min.x <= o.min.x && max.x >= o.max.x &&
               min.y <= o.min.y && max.y >= o.max.y &&
               min.z <= o.min.z && max.z >= o.max.z;
    }

    /**
     * center — Środek geometryczny AABB / Geometric center of the AABB
     */
    Vec3 center() const {
        return {(min.x + max.x) * 0.5f,
                (min.y + max.y) * 0.5f,
                (min.z + max.z) * 0.5f};
    }

    /**
     * size — Wymiary AABB (szerokość, wysokość, głębokość)
     *        Dimensions of the AABB (width, height, depth)
     */
    Vec3 size() const { return max - min; }
};

// ─────────────────────────────────────────────────────────────────────────────
// Scene Object — Obiekt sceny / Scene entity
// ─────────────────────────────────────────────────────────────────────────────

/**
 * SceneObject — Reprezentacja pojedynczego obiektu 3D w scenie
 *               Representation of a single 3D object in the scene
 *
 * Przechowuje identyfikator, transformację (pozycja, rotacja, skala),
 * wymiary bounding-box w przestrzeni modelu, wagę oraz obliczony AABB
 * w przestrzeni świata. Pozycja jest zawsze przyciągnięta do siatki.
 *
 * Stores identifier, transform (position, rotation, scale), model-space
 * bounding-box dimensions, weight, and the computed world-space AABB.
 * Position is always snapped to the grid.
 */
struct SceneObject {
    uint32_t id       = 0;        // Unikalny identyfikator obiektu / Unique object ID
    uint32_t modelId  = 0;        // ID modelu 3D (katalog mebli) / 3D model ID (furniture catalog)
    Vec3 position;                // Pozycja w świecie w cm (przyciągnięta do siatki)
                                  // World position in cm (snapped to grid)
    Vec3 rotation;                // Rotacja Eulera w stopniach / Euler rotation in degrees
    Vec3 scale;                   // Skala (jednolita lub per-oś) / Scale (uniform or per-axis)
    Vec3 bboxSize;                // Rozmiar bbox w przestrzeni modelu w cm
                                  // Model-space bounding box size in cm
    float weight      = 0.0f;    // Waga obiektu w kg / Object weight in kg
    AABB worldAABB;               // AABB w przestrzeni świata — przeliczany po każdej transformacji
                                  // World-space AABB — recomputed after every transform
};

// ─────────────────────────────────────────────────────────────────────────────
// Octree — Drzewo ósemkowe do indeksowania przestrzennego
//          Octree for spatial indexing
// ─────────────────────────────────────────────────────────────────────────────

/**
 * OCTREE_MAX_DEPTH — Maksymalna głębokość drzewa ósemkowego
 *                    Maximum depth of the octree
 *
 * Przy głębokości 10, najmniejszy węzeł pokrywa obszar o boku
 * gridSize / 2^10 ≈ gridSize / 1024. Dla siatki 10000 cm (100m)
 * daje to ~9.8 cm — blisko precyzji centymetrowej.
 *
 * At depth 10, the smallest node covers gridSize / 2^10 ≈ gridSize / 1024.
 * For a 10000 cm (100m) grid, that's ~9.8 cm — near centimeter precision.
 */
static constexpr int OCTREE_MAX_DEPTH  = 10;

/**
 * OCTREE_MAX_OBJECTS — Maks. liczba obiektów w węźle przed podziałem
 *                      Max objects in a node before subdivision
 *
 * Wartość 8 to typowy kompromis: wystarczająco mało, by zapytania
 * liniowe w liściu były szybkie, a zarazem wystarczająco dużo,
 * by unikać nadmiernego podziału przy małych scenach.
 *
 * Value of 8 is a typical trade-off: small enough for fast linear
 * scans in leaf nodes, large enough to avoid excessive subdivision
 * for small scenes.
 */
static constexpr int OCTREE_MAX_OBJECTS = 8;

/**
 * OctreeNode — Węzeł drzewa ósemkowego / Octree node
 *
 * Drzewo ósemkowe (octree) rekurencyjnie dzieli przestrzeń 3D na 8 oktantów.
 * Każdy węzeł odpowiada za prostopadłościenny region (bounds) i zawiera
 * albo listę obiektów (liść), albo 8 podwęzłów (węzeł wewnętrzny).
 *
 * An octree recursively subdivides 3D space into 8 octants. Each node
 * manages a cuboid region (bounds) and contains either a list of object IDs
 * (leaf) or 8 child nodes (internal node).
 *
 * Złożoność / Complexity:
 *   - Wstawianie / Insert: O(log n) average, O(n) worst case (degenerate)
 *   - Zapytanie regionu / Range query: O(k + log n) where k = results
 *   - Pamięć / Memory: O(n) nodes for n objects (with bounded depth)
 *
 * Uwaga implementacyjna / Implementation note:
 *   Węzły potomne przechowywane jako unique_ptr — automatyczne zwalnianie
 *   pamięci przy usunięciu lub przebudowie drzewa (RAII).
 *   Child nodes stored as unique_ptr — automatic memory deallocation
 *   on deletion or tree rebuild (RAII).
 */
class OctreeNode {
public:
    AABB bounds;                            // Region przestrzeni obsługiwany przez ten węzeł
                                            // Spatial region managed by this node
    int depth;                              // Głębokość w drzewie (0 = korzeń)
                                            // Depth in the tree (0 = root)
    std::vector<uint32_t> objectIds;        // ID obiektów przechowywanych w tym węźle (liść)
                                            // Object IDs stored in this node (leaf)
    std::unique_ptr<OctreeNode> children[8]; // 8 podwęzłów (oktantów) / 8 child nodes (octants)
    bool subdivided = false;                // Czy węzeł został podzielony / Whether node has been subdivided

    /**
     * Konstruktor / Constructor
     * @param b  Granice regionu / Region bounds (AABB)
     * @param d  Głębokość węzła / Node depth
     */
    OctreeNode(AABB b, int d) : bounds(b), depth(d) {}

    /**
     * subdivide — Dzieli węzeł na 8 podwęzłów (oktantów)
     *             Subdivides the node into 8 child octants
     *
     * Algorytm / Algorithm:
     *   1. Oblicz środek (center) bieżącego AABB
     *   2. Utwórz 8 mniejszych AABB, po jednym na oktant
     *   3. Każdy oktant to kombinacja (min|center) × (center|max) na każdej osi
     *
     * Układ oktantów / Octant layout (znaki = strona względem center):
     *   0: (---) min-min-min → center
     *   1: (+--) center-x,min-y,min-z → max-x,center-y,center-z
     *   2: (-+-) min-x,center-y,min-z → center-x,max-y,center-z
     *   3: (++-) center-x,center-y,min-z → max-x,max-y,center-z
     *   4: (--+) min-x,min-y,center-z → center-x,center-y,max-z
     *   5: (+-+) center-x,min-y,center-z → max-x,center-y,max-z
     *   6: (-++) min-x,center-y,center-z → center-x,max-y,max-z
     *   7: (+++) center → max
     */
    void subdivide() {
        Vec3 c = bounds.center();
        Vec3 mn = bounds.min, mx = bounds.max;

        // 8 oktantów — każdy zdefiniowany parą (min, max) narożników
        // 8 octants — each defined by a (min, max) corner pair
        Vec3 corners[8][2] = {
            {{mn.x, mn.y, mn.z}, {c.x,  c.y,  c.z }},  // 0: ---
            {{c.x,  mn.y, mn.z}, {mx.x, c.y,  c.z }},  // 1: +--
            {{mn.x, c.y,  mn.z}, {c.x,  mx.y, c.z }},  // 2: -+-
            {{c.x,  c.y,  mn.z}, {mx.x, mx.y, c.z }},  // 3: ++-
            {{mn.x, mn.y, c.z }, {c.x,  c.y,  mx.z}},  // 4: --+
            {{c.x,  mn.y, c.z }, {mx.x, c.y,  mx.z}},  // 5: +--+
            {{mn.x, c.y,  c.z }, {c.x,  mx.y, mx.z}},  // 6: -++
            {{c.x,  c.y,  c.z }, {mx.x, mx.y, mx.z}},  // 7: +++
        };

        for (int i = 0; i < 8; ++i) {
            children[i] = std::make_unique<OctreeNode>(
                AABB(corners[i][0], corners[i][1]), depth + 1);
        }
        subdivided = true;
    }

    /**
     * insert — Wstawia obiekt do drzewa na podstawie jego AABB
     *          Inserts an object into the tree based on its AABB
     *
     * @param objId      ID obiektu / Object ID
     * @param objBounds  AABB obiektu w przestrzeni świata / Object's world-space AABB
     *
     * Algorytm / Algorithm:
     *   1. Jeśli AABB obiektu nie przecina regionu tego węzła → pomiń (early exit)
     *   2. Jeśli węzeł jest liściem I (osiągnięto max głębokość LUB jest miejsce) →
     *      dodaj ID do listy tego węzła
     *   3. W przeciwnym razie podziel węzeł (jeśli jeszcze nie podzielony)
     *      i wstaw obiekt do wszystkich podwęzłów, które przecina
     *
     * Uwaga: Obiekt może trafić do wielu węzłów jeśli jego AABB przecina
     * granice kilku oktantów. Deduplikacja odbywa się przy zapytaniach.
     *
     * Note: An object may be inserted into multiple nodes if its AABB spans
     * octant boundaries. Deduplication happens at query time.
     */
    void insert(uint32_t objId, const AABB& objBounds) {
        // Krok 1: Wczesne wyjście jeśli brak przecięcia
        // Step 1: Early exit if no intersection
        if (!bounds.intersects(objBounds)) return;

        // Krok 2: Jeśli liść i jest miejsce (lub max głębokość) → zapisz tutaj
        // Step 2: If leaf and has capacity (or max depth reached) → store here
        if (!subdivided && (depth >= OCTREE_MAX_DEPTH ||
            (int)objectIds.size() < OCTREE_MAX_OBJECTS)) {
            objectIds.push_back(objId);
            return;
        }

        // Krok 3: Podziel węzeł jeśli potrzeba i wstaw do podwęzłów
        // Step 3: Subdivide if needed and insert into children
        if (!subdivided) {
            subdivide();
            // Uproszczenie: istniejące obiekty zostają na tym poziomie,
            // ponieważ nie mamy dostępu do ich AABB.
            // Simplification: existing objects stay at this level
            // since we don't have access to their AABBs here.
            auto old = std::move(objectIds);
            objectIds.clear();
            for (auto id : old) {
                // W praktyce potrzebowalibyśmy lookup do mapy obiektów
                // In practice, we'd need a lookup into the objects map
                objectIds.push_back(id);
            }
        }

        // Wstaw do wszystkich podwęzłów, których region przecina AABB obiektu
        // Insert into all children whose regions overlap the object's AABB
        for (int i = 0; i < 8; ++i) {
            if (children[i] && children[i]->bounds.intersects(objBounds)) {
                children[i]->insert(objId, objBounds);
            }
        }
    }

    /**
     * query — Zapytanie regionowe: znajduje wszystkie obiekty w danym AABB
     *         Range query: finds all objects within a given AABB region
     *
     * @param region   Region zapytania / Query region (AABB)
     * @param results  Wektor wynikowy (mogą się powtarzać!) / Result vector (may have duplicates!)
     *
     * Algorytm / Algorithm:
     *   1. Jeśli region nie przecina tego węzła → pomiń
     *   2. Dodaj wszystkie ID z tego węzła do wyników
     *   3. Rekurencyjnie odpytuj wszystkie podwęzły
     *
     * Uwaga: Wyniki mogą zawierać duplikaty, ponieważ obiekt może
     * znajdować się w wielu węzłach. Wywołujący musi deduplikować.
     *
     * Note: Results may contain duplicates since an object can exist
     * in multiple nodes. Caller must deduplicate.
     *
     * Złożoność / Complexity: O(k + nodes_visited), where k = results
     */
    void query(const AABB& region, std::vector<uint32_t>& results) const {
        // Wczesne wyjście / Early exit
        if (!bounds.intersects(region)) return;

        // Dodaj obiekty z tego węzła / Add objects from this node
        for (auto id : objectIds) {
            results.push_back(id);
        }

        // Rekurencyjne zapytanie do podwęzłów / Recursively query children
        if (subdivided) {
            for (int i = 0; i < 8; ++i) {
                if (children[i]) children[i]->query(region, results);
            }
        }
    }

    /**
     * clear — Czyści węzeł i wszystkie podwęzły / Clears node and all children
     *
     * Usuwa wszystkie ID obiektów i zwalnia podwęzły (unique_ptr::reset).
     * Removes all object IDs and deallocates children (unique_ptr::reset).
     */
    void clear() {
        objectIds.clear();
        for (int i = 0; i < 8; ++i) children[i].reset();
        subdivided = false;
    }
};

// ─────────────────────────────────────────────────────────────────────────────
// Result structs — Struktury wynikowe zwracane do JS
//                  Result structs returned to JavaScript
// ─────────────────────────────────────────────────────────────────────────────

/**
 * CollisionResult — Wynik detekcji kolizji / Collision detection result
 *
 * Zwraca czy obiekt koliduje z innymi oraz listę ID kolidujących obiektów.
 * Returns whether an object collides with others and a list of colliding IDs.
 */
struct CollisionResult {
    bool hasCollision = false;             // Czy wykryto kolizję / Whether collision detected
    std::vector<uint32_t> collidingIds;    // Lista kolidujących obiektów / List of colliding object IDs
};

/**
 * PhysicsResult — Wynik obliczeń fizycznych / Physics calculation result
 *
 * Zawiera sumaryczną wagę sceny, środek ciężkości, ocenę równowagi
 * oraz informację o stabilności i obciążeniu na jednostkę powierzchni.
 *
 * Contains total scene weight, center of mass, balance score,
 * stability flag, and load per area metric.
 */
struct PhysicsResult {
    float totalWeight     = 0.0f;  // Sumaryczna waga w kg / Total weight in kg
    Vec3  centerOfMass;            // Środek ciężkości (ważona pozycja) / Center of mass (weighted position)
    float balanceScore    = 1.0f;  // Ocena równowagi 0..1 (1 = idealna)
                                   // Balance score 0..1 (1 = perfect balance)
    bool  isStable        = true;  // Czy układ jest stabilny (środek ciężkości nad podporą)
                                   // Whether arrangement is stable (CoM over support polygon)
    float maxLoadPerArea  = 0.0f;  // Obciążenie w kg/cm² / Load in kg per cm²
};

/**
 * SnapResult — Wynik przyciągania do siatki / Grid snap result
 *
 * Zwraca współrzędne po zaokrągleniu do najbliższego punktu siatki.
 * Returns coordinates after rounding to the nearest grid point.
 */
struct SnapResult {
    float x, y, z;
};

// ─────────────────────────────────────────────────────────────────────────────
// Binary format — Format binarny serializacji sceny
//                 Binary scene serialization format
// ─────────────────────────────────────────────────────────────────────────────
//
// Własny format binarny "BL3D" do zapisywania i wczytywania scen.
// Custom binary "BL3D" format for saving and loading scenes.
//
// Struktura / Layout:
//
// Header (20 bajtów / bytes):
//   magic   u32  0x424C3344  ("BL3D" — identyfikator formatu / format identifier)
//   version u16  1           (wersja formatu / format version)
//   flags   u16  0           (zarezerwowane na przyszłość / reserved for future use)
//   gridW   f32  cm          (szerokość siatki / grid width)
//   gridH   f32  cm          (wysokość siatki / grid height)
//   gridD   f32  cm          (głębokość siatki / grid depth)
//
// Object count (4 bajty / bytes):
//   count   u32              (liczba obiektów / number of objects)
//
// Per object (48 bajtów / bytes each):
//   id        u32            (identyfikator obiektu / object ID)
//   modelId   u32            (identyfikator modelu / model ID)
//   posX      f32  posY f32  posZ f32  (pozycja / position)
//   rotX      f32  rotY f32  rotZ f32  (rotacja / rotation)
//   sclX      f32  sclY f32  sclZ f32  (skala / scale)
//   weight    f32            (waga w kg / weight in kg)
//
// Łączny rozmiar / Total size: 24 + count * 48 bajtów / bytes
//

/** Magic number formatu BL3D / BL3D format magic number: ASCII "BL3D" */
static constexpr uint32_t BL3D_MAGIC   = 0x424C3344;

/** Bieżąca wersja formatu / Current format version */
static constexpr uint16_t BL3D_VERSION = 1;

// ─────────────────────────────────────────────────────────────────────────────
// SceneEngine — Główna klasa silnika sceny / Main scene engine class
// ─────────────────────────────────────────────────────────────────────────────

/**
 * SceneEngine — Silnik sceny 3D / 3D Scene Engine
 *
 * Centralna klasa zarządzająca sceną 3D. Odpowiada za:
 *   - Zarządzanie obiektami (dodawanie, przesuwanie, obracanie, skalowanie, usuwanie)
 *   - Przyciąganie do siatki (snap-to-grid) z konfigurowalną rozdzielczością
 *   - Detekcję kolizji AABB z przyspieszeniem octree
 *   - Obliczenia fizyczne (waga, środek ciężkości, równowaga, obciążenie)
 *   - Serializację / deserializację do własnego formatu binarnego BL3D
 *
 * Central class managing a 3D scene. Responsible for:
 *   - Object management (add, move, rotate, scale, remove)
 *   - Snap-to-grid with configurable cell size
 *   - AABB collision detection accelerated by octree spatial index
 *   - Physics calculations (weight, center of mass, balance, structural load)
 *   - Serialization / deserialization to custom BL3D binary format
 *
 * Przechowywanie obiektów / Object storage:
 *   unordered_map<uint32_t, SceneObject> — O(1) dostęp po ID,
 *   amortyzowane O(1) wstawianie i usuwanie.
 *   unordered_map<uint32_t, SceneObject> — O(1) ID lookup,
 *   amortized O(1) insert and erase.
 *
 * Indeks przestrzenny / Spatial index:
 *   Octree przebudowywane po każdej zmianie transformacji obiektu.
 *   W obecnej implementacji pełna przebudowa (rebuildOctree) — prostsze
 *   i wystarczające dla scen o umiarkowanej liczbie obiektów.
 *   Octree rebuilt after every object transform change. Current implementation
 *   does a full rebuild — simpler and sufficient for moderately-sized scenes.
 */
class SceneEngine {
public:
    /**
     * Konstruktor / Constructor
     * @param gridW    Szerokość siatki w cm / Grid width in cm
     * @param gridH    Wysokość siatki w cm / Grid height in cm
     * @param gridD    Głębokość siatki w cm / Grid depth in cm
     * @param cellSize Rozmiar komórki siatki w cm / Grid cell size in cm
     */
    SceneEngine(float gridW, float gridH, float gridD, float cellSize);
    ~SceneEngine() = default;

    // ─── Siatka / Grid ───

    /**
     * snapToGrid — Przyciąga współrzędne do najbliższego punktu siatki
     *              Snaps coordinates to the nearest grid point
     * @return SnapResult z zaokrąglonymi współrzędnymi / with rounded coordinates
     */
    SnapResult snapToGrid(float x, float y, float z) const;

    /**
     * isInsideGrid — Sprawdza czy punkt jest wewnątrz siatki
     *                Checks whether a point is inside the grid boundaries
     */
    bool isInsideGrid(float x, float y, float z) const;

    // ─── Zarządzanie obiektami / Object management ───

    /**
     * addObject — Dodaje nowy obiekt do sceny
     *             Adds a new object to the scene
     *
     * Pozycja jest automatycznie przyciągana do siatki. Oblicza AABB
     * w przestrzeni świata i wstawia do octree.
     *
     * Position is automatically snapped to grid. Computes world-space AABB
     * and inserts into octree.
     *
     * @param modelId  ID modelu z katalogu / Model ID from catalog
     * @param pos*     Pozycja (X,Y,Z) w cm / Position (X,Y,Z) in cm
     * @param rot*     Rotacja (X,Y,Z) w stopniach / Rotation (X,Y,Z) in degrees
     * @param scl*     Skala (X,Y,Z) / Scale (X,Y,Z)
     * @param bbox*    Rozmiar bounding-box modelu (W,H,D) w cm / Model bbox size in cm
     * @param weight   Waga w kg / Weight in kg
     * @return         Unikalny ID nowego obiektu / Unique ID of the new object
     */
    uint32_t addObject(uint32_t modelId,
                       float posX, float posY, float posZ,
                       float rotX, float rotY, float rotZ,
                       float sclX, float sclY, float sclZ,
                       float bboxW, float bboxH, float bboxD,
                       float weight);

    /**
     * moveObject — Przesuwa obiekt na nową pozycję (z snap-to-grid)
     *              Moves object to new position (with snap-to-grid)
     * @return true jeśli obiekt istnieje / true if object exists
     */
    bool moveObject(uint32_t id, float x, float y, float z);

    /**
     * rotateObject — Ustawia nową rotację obiektu
     *                Sets new object rotation
     * @return true jeśli obiekt istnieje / true if object exists
     */
    bool rotateObject(uint32_t id, float rx, float ry, float rz);

    /**
     * scaleObject — Ustawia nową skalę obiektu
     *               Sets new object scale
     * @return true jeśli obiekt istnieje / true if object exists
     */
    bool scaleObject(uint32_t id, float sx, float sy, float sz);

    /**
     * removeObject — Usuwa obiekt ze sceny i przebudowuje octree
     *                Removes object from scene and rebuilds octree
     * @return true jeśli obiekt istniał / true if object existed
     */
    bool removeObject(uint32_t id);

    // ─── Detekcja kolizji / Collision detection ───

    /**
     * checkCollision — Sprawdza kolizje danego obiektu ze wszystkimi innymi
     *                  Checks collisions of a given object against all others
     *
     * Wykorzystuje octree do zawężenia kandydatów (broad phase),
     * następnie precyzyjny test AABB (narrow phase).
     * Uses octree for candidate narrowing (broad phase),
     * then precise AABB test (narrow phase).
     */
    CollisionResult checkCollision(uint32_t objectId) const;

    /**
     * checkCollisionAt — Sprawdza kolizje hipotetycznego obiektu w danym punkcie
     *                    Checks collisions of a hypothetical object at a given position
     *
     * Przydatne do podglądu czy obiekt zmieści się w danym miejscu
     * przed jego umieszczeniem.
     * Useful for previewing whether an object would fit at a position
     * before placing it.
     *
     * @param x,y,z      Pozycja (przyciągana do siatki) / Position (snapped to grid)
     * @param bbox*       Wymiary bbox / Bbox dimensions
     * @param excludeId   ID obiektu do wykluczenia (0 = brak) / Object ID to exclude (0 = none)
     */
    CollisionResult checkCollisionAt(float x, float y, float z,
                                     float bboxW, float bboxH, float bboxD,
                                     uint32_t excludeId) const;

    // ─── Fizyka / Physics ───

    /**
     * calculatePhysics — Oblicza parametry fizyczne całej sceny
     *                    Calculates physics parameters for the entire scene
     *
     * Oblicza: sumaryczną wagę, środek ciężkości, ocenę równowagi,
     * stabilność oraz obciążenie na jednostkę powierzchni.
     *
     * Computes: total weight, center of mass, balance score,
     * stability flag, and load per unit area.
     */
    PhysicsResult calculatePhysics() const;

    /**
     * getLoadAtPoint — Oblicza obciążenie w danym punkcie (XZ) od obiektów powyżej
     *                  Calculates load at a given point (XZ) from objects above
     *
     * Sumuje wagę obiektów, których AABB w rzucie XZ zawiera dany punkt
     * i które znajdują się powyżej podanej wysokości y.
     *
     * Sums weight of objects whose XZ AABB projection contains the point
     * and which are above the given y height.
     *
     * @return Obciążenie w kg / Load in kg
     */
    float getLoadAtPoint(float x, float y, float z) const;

    // ─── Serializacja / Serialization ───

    /**
     * serialize — Zapisuje scenę do formatu binarnego BL3D
     *             Serializes the scene to BL3D binary format
     * @return Bufor bajtów / Byte buffer
     */
    std::vector<uint8_t> serialize() const;

    /**
     * deserialize — Wczytuje scenę z formatu binarnego BL3D
     *               Deserializes the scene from BL3D binary format
     *
     * Zastępuje bieżącą scenę danymi z bufora. Waliduje magic number
     * i wersję formatu.
     * Replaces current scene with data from buffer. Validates magic number
     * and format version.
     *
     * @param data    Wskaźnik na dane / Pointer to data
     * @param length  Rozmiar danych w bajtach / Data size in bytes
     * @return true jeśli deserializacja się powiodła / true if deserialization succeeded
     */
    bool deserialize(const uint8_t* data, size_t length);

    // ─── Zapytania / Queries ───

    /** Zwraca liczbę obiektów w scenie / Returns number of objects in the scene */
    int getObjectCount() const;

    /** Zwraca listę ID wszystkich obiektów / Returns list of all object IDs */
    std::vector<uint32_t> getAllObjectIds() const;

    /**
     * getObjectData — Pobiera dane obiektu po ID
     *                 Retrieves object data by ID
     *
     * Wypełnia wskazane bufory danymi obiektu. Wszystkie wskaźniki muszą
     * być prawidłowe (non-null).
     * Fills pointed buffers with object data. All pointers must be valid (non-null).
     *
     * @return true jeśli obiekt istnieje / true if object exists
     */
    bool getObjectData(uint32_t id,
                       float* outPosX, float* outPosY, float* outPosZ,
                       float* outRotX, float* outRotY, float* outRotZ,
                       float* outSclX, float* outSclY, float* outSclZ,
                       uint32_t* outModelId, float* outWeight) const;

    // ─── Informacje o siatce / Grid info ───

    /** Szerokość siatki w cm / Grid width in cm */
    float getGridWidth() const  { return gridW_; }
    /** Wysokość siatki w cm / Grid height in cm */
    float getGridHeight() const { return gridH_; }
    /** Głębokość siatki w cm / Grid depth in cm */
    float getGridDepth() const  { return gridD_; }
    /** Rozmiar komórki siatki w cm / Grid cell size in cm */
    float getCellSize() const   { return cellSize_; }

private:
    float gridW_, gridH_, gridD_;   // Wymiary siatki w cm / Grid dimensions in cm
    float cellSize_;                 // Rozmiar komórki w cm / Cell size in cm
    uint32_t nextId_ = 1;           // Następny wolny ID obiektu (autoinkrementacja)
                                     // Next free object ID (auto-increment)

    std::unordered_map<uint32_t, SceneObject> objects_;  // Mapa obiektów: ID → SceneObject
                                                          // Object map: ID → SceneObject
                                                          // O(1) average lookup, insert, erase

    std::unique_ptr<OctreeNode> octree_;                  // Korzeń drzewa ósemkowego
                                                          // Octree root node

    /**
     * rebuildOctree — Przebudowuje octree od zera
     *                 Rebuilds the octree from scratch
     *
     * Wywoływane po każdej zmianie transformacji obiektu.
     * Called after every object transform change.
     */
    void rebuildOctree();

    /**
     * computeWorldAABB — Oblicza AABB w przestrzeni świata dla danego obiektu
     *                    Computes world-space AABB for a given object
     *
     * Uwzględnia skalę, rotację (przez macierz obrotów) i pozycję.
     * Accounts for scale, rotation (via rotation matrix), and position.
     */
    AABB computeWorldAABB(const SceneObject& obj) const;

    /**
     * snap — Zaokrągla wartość do najbliższej wielokrotności cellSize_
     *        Rounds a value to the nearest multiple of cellSize_
     */
    float snap(float value) const;
};
