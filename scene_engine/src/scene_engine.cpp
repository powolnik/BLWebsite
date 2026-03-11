/*******************************************************************************
 * scene_engine.cpp — Implementacja silnika sceny 3D
 *                    3D Scene Engine implementation
 *
 * Projekt / Project : BLACK LIGHT Collective — 3D Scene Engine
 * Autor / Author    : BLACK LIGHT Collective
 * Opis / Description:
 *   Plik zawiera implementację wszystkich metod klasy SceneEngine oraz
 *   funkcji pomocniczych. Obejmuje:
 *     - Funkcję rotateAABB do obliczania AABB po obrocie
 *     - Konstruktor silnika i inicjalizację octree
 *     - Zarządzanie obiektami (dodawanie, przesuwanie, obracanie, skalowanie, usuwanie)
 *     - Detekcję kolizji (broad-phase octree + narrow-phase AABB)
 *     - Obliczenia fizyczne (waga, środek ciężkości, równowaga, obciążenie)
 *     - Serializację / deserializację formatu BL3D
 *     - Metody zapytań o stan sceny
 *
 *   Contains implementations of all SceneEngine methods and helper functions:
 *     - rotateAABB function for computing AABB after rotation
 *     - Engine constructor and octree initialization
 *     - Object management (add, move, rotate, scale, remove)
 *     - Collision detection (broad-phase octree + narrow-phase AABB)
 *     - Physics calculations (weight, center of mass, balance, load)
 *     - BL3D format serialization / deserialization
 *     - Scene state query methods
 ******************************************************************************/

#include "scene_engine.h"
#include <cstring>    // std::memcpy — kopiowanie bajtów w serializacji / byte copying in serialization
#include <algorithm>  // std::min, std::max — obliczenia fizyczne / physics calculations
#include <set>        // std::set — deduplikacja wyników kolizji / collision result deduplication

// ═══════════════════════════════════════════════════════════════════════════════
// Helpers — Funkcje pomocnicze / Helper functions
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * rotateAABB — Oblicza nowy AABB po obróceniu prostopadłościanu
 *              Computes a new AABB after rotating a box
 *
 * @param halfSize  Połowa wymiarów (half-extents) oryginalnego bbox / Half-extents of original bbox
 * @param rotation  Kąty Eulera w stopniach (X, Y, Z) / Euler angles in degrees (X, Y, Z)
 * @return          Nowy AABB wyśrodkowany w (0,0,0) / New AABB centered at origin (0,0,0)
 *
 * Algorytm / Algorithm:
 *   1. Przelicz kąty Eulera ze stopni na radiany
 *      Convert Euler angles from degrees to radians
 *   2. Zbuduj macierz obrotu 3×3 w kolejności Y * X * Z
 *      Build 3×3 rotation matrix in Y * X * Z order
 *      (typowa kolejność dla silników gier — yaw, pitch, roll)
 *      (typical order for game engines — yaw, pitch, roll)
 *   3. Oblicz nowe half-extents jako sumę iloczynów bezwzględnych wartości
 *      macierzy z oryginalnymi half-extents (metoda "absolute rotation matrix")
 *      Compute new half-extents as sum of products of absolute matrix values
 *      with original half-extents (the "absolute rotation matrix" method)
 *
 * Ta technika jest standardowym sposobem obliczania AABB obróconych obiektów —
 * zamiast obracać 8 wierzchołków i szukać min/max, stosujemy własność
 * wartości bezwzględnej: |M * v| <= |M| * |v| (nierówność trójkąta).
 *
 * This technique is the standard way to compute AABBs of rotated objects —
 * instead of rotating 8 vertices and finding min/max, we exploit the
 * absolute value property: |M * v| <= |M| * |v| (triangle inequality).
 *
 * Wynikowy AABB zawsze obejmuje obrócony obiekt, ale jest zazwyczaj
 * nieco większy niż potrzebny (conservative bound).
 *
 * The resulting AABB always encloses the rotated object but is typically
 * slightly larger than necessary (conservative bound).
 */
static AABB rotateAABB(const Vec3& halfSize, const Vec3& rotation) {
    // Krok 1: Konwersja stopni → radiany / Step 1: Convert degrees → radians
    float rx = rotation.x * (3.14159265f / 180.0f);
    float ry = rotation.y * (3.14159265f / 180.0f);
    float rz = rotation.z * (3.14159265f / 180.0f);

    // Krok 2: Oblicz funkcje trygonometryczne / Step 2: Compute trig functions
    // Precompute sin/cos for all three axes (cheaper than repeated calls)
    float cy = std::cos(ry), sy = std::sin(ry);
    float cx = std::cos(rx), sx = std::sin(rx);
    float cz = std::cos(rz), sz = std::sin(rz);

    // Krok 3: Macierz obrotu (kolejność Y * X * Z)
    // Step 3: Rotation matrix (Y * X * Z order)
    //
    // Macierz łączy trzy obroty w jedną transformację:
    //   R = Ry(ry) * Rx(rx) * Rz(rz)
    // The matrix combines three rotations into one transform:
    //   R = Ry(ry) * Rx(rx) * Rz(rz)
    float m[3][3] = {
        { cy*cz + sy*sx*sz,  -cy*sz + sy*sx*cz,  sy*cx },
        { cx*sz,              cx*cz,             -sx    },
        {-sy*cz + cy*sx*sz,   sy*sz + cy*sx*cz,  cy*cx }
    };

    // Krok 4: Nowe half-extents z macierzy bezwzględnej
    // Step 4: New half-extents from absolute matrix
    //
    // Dla każdej osi wynikowej, nowy half-extent to suma:
    //   |m[row][0]| * halfSize.x + |m[row][1]| * halfSize.y + |m[row][2]| * halfSize.z
    //
    // For each output axis, the new half-extent is the sum:
    //   |m[row][0]| * halfSize.x + |m[row][1]| * halfSize.y + |m[row][2]| * halfSize.z
    Vec3 newHalf;
    newHalf.x = std::abs(m[0][0]) * halfSize.x + std::abs(m[0][1]) * halfSize.y + std::abs(m[0][2]) * halfSize.z;
    newHalf.y = std::abs(m[1][0]) * halfSize.x + std::abs(m[1][1]) * halfSize.y + std::abs(m[1][2]) * halfSize.z;
    newHalf.z = std::abs(m[2][0]) * halfSize.x + std::abs(m[2][1]) * halfSize.y + std::abs(m[2][2]) * halfSize.z;

    // Zwróć AABB wyśrodkowany w (0,0,0) — będzie przesunięty o pozycję obiektu
    // Return AABB centered at origin — will be translated by object position
    return AABB(Vec3(-newHalf.x, -newHalf.y, -newHalf.z),
                Vec3( newHalf.x,  newHalf.y,  newHalf.z));
}

// ═══════════════════════════════════════════════════════════════════════════════
// SceneEngine — Konstruktor i metody siatki
//               Constructor and grid methods
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Konstruktor SceneEngine — Inicjalizacja silnika
 *                           Engine initialization
 *
 * Tworzy scenę o podanych wymiarach siatki i inicjalizuje korzeń octree
 * z AABB obejmującym całą siatkę. Wszystkie wymiary w centymetrach.
 *
 * Creates a scene with given grid dimensions and initializes the octree
 * root with an AABB encompassing the entire grid. All dimensions in cm.
 */
SceneEngine::SceneEngine(float gridW, float gridH, float gridD, float cellSize)
    : gridW_(gridW), gridH_(gridH), gridD_(gridD), cellSize_(cellSize)
{
    // Korzeń octree obejmuje całą siatkę: od (0,0,0) do (gridW, gridH, gridD)
    // Octree root covers the entire grid: from (0,0,0) to (gridW, gridH, gridD)
    AABB worldBounds(Vec3(0, 0, 0), Vec3(gridW, gridH, gridD));
    octree_ = std::make_unique<OctreeNode>(worldBounds, 0);
}

/**
 * snap — Zaokrągla wartość do najbliższej wielokrotności cellSize_
 *        Rounds a value to the nearest multiple of cellSize_
 *
 * Wzór / Formula: round(value / cellSize) * cellSize
 * Np. / E.g.: snap(7.3, cellSize=5.0) → round(1.46) * 5 = 1 * 5 = 5.0
 */
float SceneEngine::snap(float value) const {
    return std::round(value / cellSize_) * cellSize_;
}

/**
 * snapToGrid — Przyciąga punkt (x,y,z) do siatki
 *              Snaps point (x,y,z) to the grid
 *
 * Każda współrzędna jest niezależnie zaokrąglana do siatki.
 * Each coordinate is independently rounded to the grid.
 */
SnapResult SceneEngine::snapToGrid(float x, float y, float z) const {
    return { snap(x), snap(y), snap(z) };
}

/**
 * isInsideGrid — Sprawdza czy punkt mieści się w granicach siatki
 *                Checks whether a point lies within grid boundaries
 *
 * Siatka rozciąga się od (0,0,0) do (gridW_, gridH_, gridD_).
 * Granice są inkluzywne (inclusive bounds).
 *
 * The grid extends from (0,0,0) to (gridW_, gridH_, gridD_).
 * Boundaries are inclusive.
 */
bool SceneEngine::isInsideGrid(float x, float y, float z) const {
    return x >= 0 && x <= gridW_ &&
           y >= 0 && y <= gridH_ &&
           z >= 0 && z <= gridD_;
}

/**
 * computeWorldAABB — Oblicza AABB obiektu w przestrzeni świata
 *                    Computes an object's world-space AABB
 *
 * Algorytm / Algorithm:
 *   1. Oblicz half-extents z bboxSize i scale
 *      Compute half-extents from bboxSize and scale
 *   2. Zastosuj rotację (rotateAABB) — wynik jest AABB wyśrodkowany w (0,0,0)
 *      Apply rotation (rotateAABB) — result is AABB centered at origin
 *   3. Przesuń o pozycję obiektu (translacja)
 *      Translate by object position
 */
AABB SceneEngine::computeWorldAABB(const SceneObject& obj) const {
    // Krok 1: Half-extents = (bboxSize * scale) / 2
    Vec3 halfSize(
        obj.bboxSize.x * obj.scale.x * 0.5f,
        obj.bboxSize.y * obj.scale.y * 0.5f,
        obj.bboxSize.z * obj.scale.z * 0.5f
    );

    // Krok 2: Oblicz AABB po obrocie (wyśrodkowany w origin)
    // Step 2: Compute rotated AABB (centered at origin)
    AABB rotated = rotateAABB(halfSize, obj.rotation);

    // Krok 3: Przesuń do pozycji obiektu w świecie
    // Step 3: Translate to object's world position
    return AABB(
        Vec3(obj.position.x + rotated.min.x,
             obj.position.y + rotated.min.y,
             obj.position.z + rotated.min.z),
        Vec3(obj.position.x + rotated.max.x,
             obj.position.y + rotated.max.y,
             obj.position.z + rotated.max.z)
    );
}

/**
 * rebuildOctree — Przebudowuje drzewo ósemkowe od zera
 *                 Rebuilds the octree from scratch
 *
 * Tworzy nowy korzeń i wstawia wszystkie obiekty. Przy okazji
 * przelicza worldAABB każdego obiektu.
 *
 * Creates a new root and inserts all objects. Also recomputes
 * each object's worldAABB in the process.
 *
 * Złożoność / Complexity: O(n * log n) average, O(n²) worst case
 * Wywoływane po: moveObject, rotateObject, scaleObject, removeObject, deserialize
 * Called after: moveObject, rotateObject, scaleObject, removeObject, deserialize
 */
void SceneEngine::rebuildOctree() {
    AABB worldBounds(Vec3(0, 0, 0), Vec3(gridW_, gridH_, gridD_));
    octree_ = std::make_unique<OctreeNode>(worldBounds, 0);
    for (auto& [id, obj] : objects_) {
        obj.worldAABB = computeWorldAABB(obj);
        octree_->insert(id, obj.worldAABB);
    }
}

// ═══════════════════════════════════════════════════════════════════════════════
// Object Management — Zarządzanie obiektami
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * addObject — Dodaje nowy obiekt do sceny
 *             Adds a new object to the scene
 *
 * Kroki / Steps:
 *   1. Tworzy SceneObject z autoinkrementowanym ID
 *      Creates SceneObject with auto-incremented ID
 *   2. Przyciąga pozycję do siatki (snap)
 *      Snaps position to grid
 *   3. Oblicza world AABB
 *      Computes world AABB
 *   4. Dodaje do mapy obiektów i octree
 *      Adds to object map and octree
 *
 * Uwaga: Nie przebudowuje całego octree — wystarczy insert do istniejącego.
 * Note: Does not rebuild entire octree — single insert into existing tree suffices.
 */
uint32_t SceneEngine::addObject(
    uint32_t modelId,
    float posX, float posY, float posZ,
    float rotX, float rotY, float rotZ,
    float sclX, float sclY, float sclZ,
    float bboxW, float bboxH, float bboxD,
    float weight)
{
    SceneObject obj;
    obj.id       = nextId_++;                              // Autoinkrementacja ID / Auto-increment ID
    obj.modelId  = modelId;                                // ID modelu z katalogu mebli / Furniture catalog model ID
    obj.position = Vec3(snap(posX), snap(posY), snap(posZ)); // Pozycja przyciągnięta do siatki / Grid-snapped position
    obj.rotation = Vec3(rotX, rotY, rotZ);                 // Rotacja Eulera w stopniach / Euler rotation in degrees
    obj.scale    = Vec3(sclX, sclY, sclZ);                 // Skala per-oś / Per-axis scale
    obj.bboxSize = Vec3(bboxW, bboxH, bboxD);              // Rozmiar bbox modelu w cm / Model bbox in cm
    obj.weight   = weight;                                  // Waga w kg / Weight in kg
    obj.worldAABB = computeWorldAABB(obj);                 // Oblicz AABB świata / Compute world AABB

    objects_[obj.id] = obj;                                // Zapisz w mapie / Store in map
    octree_->insert(obj.id, obj.worldAABB);                // Wstaw do octree / Insert into octree

    return obj.id;
}

/**
 * moveObject — Przesuwa obiekt na nową pozycję
 *              Moves an object to a new position
 *
 * Nowa pozycja jest przyciągana do siatki. Po przesunięciu przebudowuje
 * octree, ponieważ AABB obiektu się zmienił.
 *
 * New position is snapped to grid. After moving, rebuilds the octree
 * since the object's AABB has changed.
 */
bool SceneEngine::moveObject(uint32_t id, float x, float y, float z) {
    auto it = objects_.find(id);
    if (it == objects_.end()) return false;  // Obiekt nie istnieje / Object doesn't exist

    it->second.position = Vec3(snap(x), snap(y), snap(z));  // Snap do siatki / Snap to grid
    it->second.worldAABB = computeWorldAABB(it->second);     // Przelicz AABB / Recompute AABB
    rebuildOctree();                                          // Przebuduj octree / Rebuild octree
    return true;
}

/**
 * rotateObject — Ustawia nową rotację obiektu
 *                Sets new rotation for an object
 *
 * Zmiana rotacji zmienia AABB (obrócony bbox ma inne wymiary w osiach).
 * Rotation change affects AABB (rotated bbox has different axis-aligned dimensions).
 */
bool SceneEngine::rotateObject(uint32_t id, float rx, float ry, float rz) {
    auto it = objects_.find(id);
    if (it == objects_.end()) return false;

    it->second.rotation = Vec3(rx, ry, rz);
    it->second.worldAABB = computeWorldAABB(it->second);
    rebuildOctree();
    return true;
}

/**
 * scaleObject — Ustawia nową skalę obiektu
 *               Sets new scale for an object
 *
 * Zmiana skali zmienia zarówno wymiary bbox jak i AABB.
 * Scale change affects both bbox dimensions and AABB.
 */
bool SceneEngine::scaleObject(uint32_t id, float sx, float sy, float sz) {
    auto it = objects_.find(id);
    if (it == objects_.end()) return false;

    it->second.scale = Vec3(sx, sy, sz);
    it->second.worldAABB = computeWorldAABB(it->second);
    rebuildOctree();
    return true;
}

/**
 * removeObject — Usuwa obiekt ze sceny
 *                Removes an object from the scene
 *
 * Po usunięciu z mapy obiektów przebudowuje octree (ponieważ octree
 * nie wspiera bezpośredniego usuwania w tej implementacji).
 *
 * After removing from the object map, rebuilds octree (since this
 * implementation doesn't support direct octree removal).
 */
bool SceneEngine::removeObject(uint32_t id) {
    auto it = objects_.find(id);
    if (it == objects_.end()) return false;

    objects_.erase(it);
    rebuildOctree();
    return true;
}

// ═══════════════════════════════════════════════════════════════════════════════
// Collision Detection — Detekcja kolizji
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * checkCollision — Sprawdza kolizje obiektu z innymi obiektami w scenie
 *                  Checks collisions of an object against others in the scene
 *
 * Algorytm dwufazowy / Two-phase algorithm:
 *
 *   Faza 1 (Broad phase — szerokie przeszukiwanie):
 *     Odpytaj octree o obiekty, których AABB przecina AABB badanego obiektu.
 *     Octree drastycznie redukuje liczbę kandydatów z O(n) do O(√n) średnio.
 *
 *   Phase 1 (Broad phase):
 *     Query octree for objects whose AABB intersects the test object's AABB.
 *     Octree drastically reduces candidate count from O(n) to O(√n) on average.
 *
 *   Faza 2 (Narrow phase — dokładne sprawdzenie):
 *     Dla każdego kandydata wykonaj precyzyjny test AABB-AABB.
 *     Deduplikacja przez std::set (obiekt może pojawić się w wielu węzłach octree).
 *
 *   Phase 2 (Narrow phase):
 *     For each candidate, perform precise AABB-AABB intersection test.
 *     Deduplication via std::set (object may appear in multiple octree nodes).
 *
 * Złożoność / Complexity: O(k log k + m) where k = octree candidates, m = collisions
 */
CollisionResult SceneEngine::checkCollision(uint32_t objectId) const {
    CollisionResult result;
    auto it = objects_.find(objectId);
    if (it == objects_.end()) return result;  // Obiekt nie istnieje / Object not found

    const AABB& aabb = it->second.worldAABB;

    // Faza 1: Zapytaj octree o kandydatów / Phase 1: Query octree for candidates
    std::vector<uint32_t> candidates;
    octree_->query(aabb, candidates);

    // Faza 2: Deduplikacja i precyzyjny test / Phase 2: Deduplicate and precise test
    std::set<uint32_t> seen;  // std::set do usuwania duplikatów / std::set for deduplication
    for (uint32_t cid : candidates) {
        if (cid == objectId) continue;   // Pomiń samego siebie / Skip self
        if (seen.count(cid)) continue;   // Pomiń duplikaty / Skip duplicates
        seen.insert(cid);

        // Precyzyjny test AABB / Precise AABB test
        auto cit = objects_.find(cid);
        if (cit != objects_.end() && aabb.intersects(cit->second.worldAABB)) {
            result.collidingIds.push_back(cid);
        }
    }

    result.hasCollision = !result.collidingIds.empty();
    return result;
}

/**
 * checkCollisionAt — Sprawdza kolizje hipotetycznego obiektu w punkcie (x,y,z)
 *                    Checks collisions of a hypothetical object at point (x,y,z)
 *
 * Tworzy tymczasowy AABB (nie dodaje obiektu do sceny) i sprawdza
 * kolizje z istniejącymi obiektami. Przydatne do walidacji przed
 * umieszczeniem obiektu.
 *
 * Creates a temporary AABB (doesn't add object to scene) and checks
 * collisions with existing objects. Useful for validation before placement.
 *
 * @param excludeId  ID obiektu do wykluczenia z testu (np. obiekt, który przesuwamy)
 *                   Object ID to exclude from test (e.g., the object being moved)
 */
CollisionResult SceneEngine::checkCollisionAt(
    float x, float y, float z,
    float bboxW, float bboxH, float bboxD,
    uint32_t excludeId) const
{
    CollisionResult result;

    // Przyciągnij pozycję do siatki / Snap position to grid
    float sx = snap(x), sy = snap(y), sz = snap(z);

    // Oblicz AABB testowy z half-extents / Compute test AABB from half-extents
    float hw = bboxW * 0.5f, hh = bboxH * 0.5f, hd = bboxD * 0.5f;
    AABB testBox(Vec3(sx - hw, sy - hh, sz - hd),
                 Vec3(sx + hw, sy + hh, sz + hd));

    // Faza 1: Zapytaj octree / Phase 1: Query octree
    std::vector<uint32_t> candidates;
    octree_->query(testBox, candidates);

    // Faza 2: Deduplikacja i precyzyjny test / Phase 2: Deduplicate and precise test
    std::set<uint32_t> seen;
    for (uint32_t cid : candidates) {
        if (cid == excludeId) continue;  // Wyklucz wskazany obiekt / Exclude specified object
        if (seen.count(cid)) continue;
        seen.insert(cid);

        auto cit = objects_.find(cid);
        if (cit != objects_.end() && testBox.intersects(cit->second.worldAABB)) {
            result.collidingIds.push_back(cid);
        }
    }

    result.hasCollision = !result.collidingIds.empty();
    return result;
}

// ═══════════════════════════════════════════════════════════════════════════════
// Physics — Obliczenia fizyczne / Physics calculations
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * calculatePhysics — Oblicza parametry fizyczne całej sceny
 *                    Calculates physics parameters for the entire scene
 *
 * Algorytm / Algorithm:
 *
 *   1. WAGA CAŁKOWITA / TOTAL WEIGHT:
 *      Suma wag wszystkich obiektów.
 *      Sum of all object weights.
 *
 *   2. ŚRODEK CIĘŻKOŚCI / CENTER OF MASS:
 *      Średnia ważona pozycji obiektów: CoM = Σ(pos_i * weight_i) / Σweight_i
 *      Weighted average of object positions: CoM = Σ(pos_i * weight_i) / Σweight_i
 *
 *   3. POLYGON PODPORY / SUPPORT POLYGON:
 *      Prostokąt (AABB w XZ) obejmujący wszystkie obiekty dotykające podłogi
 *      (dolna krawędź AABB poniżej 1 cm od y=0). To uproszczenie — prawdziwy
 *      polygon podpory jest otoczką wypukłą stóp kontaktowych.
 *
 *      Rectangle (XZ AABB) encompassing all objects touching the ground
 *      (bottom AABB edge below 1 cm from y=0). This is a simplification —
 *      the true support polygon is the convex hull of contact footprints.
 *
 *   4. OCENA RÓWNOWAGI / BALANCE SCORE:
 *      Znormalizowana odległość rzutu środka ciężkości (XZ) od środka
 *      polygonu podpory: balanceScore = max(0, 1 - dist)
 *
 *      Normalized distance of CoM projection (XZ) from support polygon center:
 *      balanceScore = max(0, 1 - dist)
 *
 *      Gdzie dist = sqrt((dx/halfW)² + (dz/halfD)²), dx/dz to odległości
 *      od środka podpory, halfW/halfD to połowy wymiarów podpory.
 *
 *      Where dist = sqrt((dx/halfW)² + (dz/halfD)²), dx/dz are distances
 *      from support center, halfW/halfD are half-dimensions of support.
 *
 *   5. STABILNOŚĆ / STABILITY:
 *      Układ jest stabilny gdy rzut środka ciężkości mieści się
 *      w polygonie podpory (dx <= 1.0, dz <= 1.0 po normalizacji).
 *
 *      System is stable when CoM projection lies within support polygon
 *      (dx <= 1.0, dz <= 1.0 after normalization).
 *
 *   6. OBCIĄŻENIE / LOAD PER AREA:
 *      Uproszczone: totalWeight / supportArea [kg/cm²]
 *      Simplified: totalWeight / supportArea [kg/cm²]
 *
 * Przypadki brzegowe / Edge cases:
 *   - Pusta scena → domyślne wartości (waga 0, balans 1.0, stabilny)
 *   - Podpora punktowa (supportW lub supportD = 0) → balans 0.1, niestabilne jeśli >5kg
 *   - Brak podpory (obiekty "latające") → balans 0.0, niestabilne
 */
PhysicsResult SceneEngine::calculatePhysics() const {
    PhysicsResult result;

    // Przypadek brzegowy: pusta scena / Edge case: empty scene
    if (objects_.empty()) return result;

    float totalW  = 0;
    Vec3 weightedPos(0, 0, 0);  // Akumulator ważonej pozycji / Weighted position accumulator

    // Zmienne do obliczenia polygonu podpory (AABB w XZ obiektów na podłodze)
    // Variables for computing support polygon (XZ AABB of ground-touching objects)
    float supportMinX = gridW_, supportMaxX = 0;
    float supportMinZ = gridD_, supportMaxZ = 0;
    bool hasSupport = false;

    // Iteracja po wszystkich obiektach — O(n)
    // Iterate over all objects — O(n)
    for (auto& [id, obj] : objects_) {
        // Akumuluj wagę i ważoną pozycję do obliczenia środka ciężkości
        // Accumulate weight and weighted position for center of mass
        totalW += obj.weight;
        weightedPos.x += obj.position.x * obj.weight;
        weightedPos.y += obj.position.y * obj.weight;
        weightedPos.z += obj.position.z * obj.weight;

        // Sprawdź czy obiekt dotyka podłogi (dolna krawędź AABB < 1 cm od y=0)
        // Check if object touches the ground (bottom AABB edge < 1 cm from y=0)
        if (obj.worldAABB.min.y < 1.0f) { // Tolerancja 1 cm / 1 cm tolerance
            hasSupport = true;
            // Rozszerz polygon podpory / Expand support polygon
            supportMinX = std::min(supportMinX, obj.worldAABB.min.x);
            supportMaxX = std::max(supportMaxX, obj.worldAABB.max.x);
            supportMinZ = std::min(supportMinZ, obj.worldAABB.min.z);
            supportMaxZ = std::max(supportMaxZ, obj.worldAABB.max.z);
        }
    }

    result.totalWeight = totalW;

    // Oblicz środek ciężkości (jeśli waga > 0)
    // Compute center of mass (if weight > 0)
    if (totalW > 0) {
        result.centerOfMass = Vec3(
            weightedPos.x / totalW,
            weightedPos.y / totalW,
            weightedPos.z / totalW
        );
    }

    // Oblicz równowagę i stabilność / Compute balance and stability
    if (hasSupport && totalW > 0) {
        // Środek i wymiary polygonu podpory / Support polygon center and dimensions
        float supportCX = (supportMinX + supportMaxX) * 0.5f;
        float supportCZ = (supportMinZ + supportMaxZ) * 0.5f;
        float supportW  = supportMaxX - supportMinX;  // Szerokość podpory / Support width
        float supportD  = supportMaxZ - supportMinZ;  // Głębokość podpory / Support depth

        if (supportW > 0 && supportD > 0) {
            // Znormalizowana odległość środka ciężkości od środka podpory
            // Normalized distance of center of mass from support center
            //
            // dx, dz ∈ [0, ∞) — wartość 1.0 oznacza krawędź podpory
            // dx, dz ∈ [0, ∞) — value 1.0 means edge of support
            float dx = std::abs(result.centerOfMass.x - supportCX) / (supportW * 0.5f);
            float dz = std::abs(result.centerOfMass.z - supportCZ) / (supportD * 0.5f);
            float dist = std::sqrt(dx * dx + dz * dz);

            // Ocena równowagi: 1.0 = idealna (CoM w środku), 0.0 = poza podporą
            // Balance score: 1.0 = perfect (CoM at center), 0.0 = outside support
            result.balanceScore = std::max(0.0f, 1.0f - dist);

            // Stabilność: CoM mieści się w prostokącie podpory
            // Stability: CoM lies within the support rectangle
            result.isStable = (dx <= 1.0f && dz <= 1.0f);

            // Obciążenie na jednostkę powierzchni (uproszczone)
            // Load per unit area (simplified)
            float supportArea = supportW * supportD;  // Powierzchnia podpory w cm²
            if (supportArea > 0) {
                result.maxLoadPerArea = totalW / supportArea;  // kg/cm²
            }
        } else {
            // Podpora punktowa — praktycznie niestabilna
            // Point support — practically unstable
            result.balanceScore = 0.1f;
            result.isStable = (totalW < 5.0f);  // Stabilne tylko dla bardzo lekkich obiektów
                                                  // Stable only for very light objects (<5 kg)
        }
    } else if (!hasSupport) {
        // Brak podpory — wszystkie obiekty "unoszą się"
        // No ground support — all objects are "floating"
        result.balanceScore = 0.0f;
        result.isStable = false;
    }

    return result;
}

/**
 * getLoadAtPoint — Oblicza obciążenie pionowe w danym punkcie
 *                  Calculates vertical load at a given point
 *
 * Przeszukuje wszystkie obiekty i sumuje wagę tych, których rzut XZ
 * zawiera punkt (x, z) i które znajdują się powyżej wysokości y.
 * Służy do oceny obciążenia konstrukcyjnego w konkretnym miejscu.
 *
 * Scans all objects and sums weight of those whose XZ projection
 * contains point (x, z) and which are above height y.
 * Used for evaluating structural load at a specific location.
 *
 * Złożoność / Complexity: O(n) — przeszukuje wszystkie obiekty
 *                                 scans all objects
 *
 * @param x, y, z  Punkt zapytania w cm / Query point in cm
 * @return         Sumaryczne obciążenie w kg / Total load in kg
 */
float SceneEngine::getLoadAtPoint(float x, float y, float z) const {
    float load = 0;
    for (auto& [id, obj] : objects_) {
        const AABB& bb = obj.worldAABB;
        // Sprawdź czy punkt (x,z) mieści się w rzucie XZ obiektu
        // i czy obiekt jest powyżej wysokości y
        // Check if point (x,z) is within object's XZ projection
        // and if object is above height y
        if (x >= bb.min.x && x <= bb.max.x &&
            z >= bb.min.z && z <= bb.max.z &&
            bb.min.y >= y) {
            load += obj.weight;
        }
    }
    return load;
}

// ═══════════════════════════════════════════════════════════════════════════════
// Serialization — Serializacja / Deserializacja sceny
//                 Scene serialization / deserialization
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * serialize — Zapisuje scenę do bufora binarnego w formacie BL3D
 *             Serializes the scene to a binary buffer in BL3D format
 *
 * Format: patrz opis w scene_engine.h (nagłówek 20B + count 4B + obiekty 48B każdy)
 * Format: see description in scene_engine.h (header 20B + count 4B + objects 48B each)
 *
 * Używa std::memcpy do zapisu wartości — bezpieczne niezależnie od endianness
 * platformy docelowej (WASM jest little-endian).
 *
 * Uses std::memcpy for writing values — safe regardless of target platform
 * endianness (WASM is little-endian).
 *
 * @return Bufor bajtów gotowy do zapisu / Byte buffer ready for saving
 */
std::vector<uint8_t> SceneEngine::serialize() const {
    // Oblicz rozmiar bufora: nagłówek (20B) + count (4B) + obiekty (48B * n)
    // Calculate buffer size: header (20B) + count (4B) + objects (48B * n)
    size_t objCount = objects_.size();
    size_t totalSize = 20 + 4 + objCount * 48;
    std::vector<uint8_t> buf(totalSize);
    uint8_t* ptr = buf.data();

    // --- Nagłówek / Header ---

    // Magic number: "BL3D" (0x424C3344)
    uint32_t magic = BL3D_MAGIC;
    std::memcpy(ptr, &magic, 4); ptr += 4;

    // Wersja formatu / Format version
    uint16_t version = BL3D_VERSION;
    std::memcpy(ptr, &version, 2); ptr += 2;

    // Flagi (zarezerwowane, obecnie 0) / Flags (reserved, currently 0)
    uint16_t flags = 0;
    std::memcpy(ptr, &flags, 2); ptr += 2;

    // Wymiary siatki w cm / Grid dimensions in cm
    std::memcpy(ptr, &gridW_, 4); ptr += 4;
    std::memcpy(ptr, &gridH_, 4); ptr += 4;
    std::memcpy(ptr, &gridD_, 4); ptr += 4;

    // --- Liczba obiektów / Object count ---
    uint32_t count = static_cast<uint32_t>(objCount);
    std::memcpy(ptr, &count, 4); ptr += 4;

    // --- Obiekty (48 bajtów każdy) / Objects (48 bytes each) ---
    for (auto& [id, obj] : objects_) {
        std::memcpy(ptr, &obj.id, 4);       ptr += 4;   // ID obiektu / Object ID
        std::memcpy(ptr, &obj.modelId, 4);   ptr += 4;   // ID modelu / Model ID
        std::memcpy(ptr, &obj.position.x, 4); ptr += 4;  // Pozycja X / Position X
        std::memcpy(ptr, &obj.position.y, 4); ptr += 4;  // Pozycja Y / Position Y
        std::memcpy(ptr, &obj.position.z, 4); ptr += 4;  // Pozycja Z / Position Z
        std::memcpy(ptr, &obj.rotation.x, 4); ptr += 4;  // Rotacja X / Rotation X
        std::memcpy(ptr, &obj.rotation.y, 4); ptr += 4;  // Rotacja Y / Rotation Y
        std::memcpy(ptr, &obj.rotation.z, 4); ptr += 4;  // Rotacja Z / Rotation Z
        std::memcpy(ptr, &obj.scale.x, 4);    ptr += 4;  // Skala X / Scale X
        std::memcpy(ptr, &obj.scale.y, 4);    ptr += 4;  // Skala Y / Scale Y
        std::memcpy(ptr, &obj.scale.z, 4);    ptr += 4;  // Skala Z / Scale Z
        std::memcpy(ptr, &obj.weight, 4);      ptr += 4;  // Waga / Weight
    }

    return buf;
}

/**
 * deserialize — Wczytuje scenę z bufora binarnego w formacie BL3D
 *               Deserializes the scene from a BL3D binary buffer
 *
 * Algorytm / Algorithm:
 *   1. Walidacja rozmiaru (minimum 24 bajty: nagłówek + count)
 *      Validate size (minimum 24 bytes: header + count)
 *   2. Sprawdź magic number i wersję formatu
 *      Check magic number and format version
 *   3. Odczytaj wymiary siatki
 *      Read grid dimensions
 *   4. Odczytaj liczbę obiektów i sprawdź czy bufor jest wystarczająco duży
 *      Read object count and verify buffer is large enough
 *   5. Wyczyść bieżącą scenę i wczytaj obiekty
 *      Clear current scene and load objects
 *   6. Zaktualizuj nextId_ na max(id) + 1
 *      Update nextId_ to max(id) + 1
 *   7. Przebuduj octree
 *      Rebuild octree
 *
 * @param data    Wskaźnik na dane binarne / Pointer to binary data
 * @param length  Długość danych w bajtach / Data length in bytes
 * @return true jeśli deserializacja się powiodła / true if deserialization succeeded
 */
bool SceneEngine::deserialize(const uint8_t* data, size_t length) {
    // Walidacja minimalnego rozmiaru / Validate minimum size
    if (length < 24) return false; // minimum: nagłówek (20B) + count (4B)

    const uint8_t* ptr = data;

    // Sprawdź magic number / Check magic number
    uint32_t magic;
    std::memcpy(&magic, ptr, 4); ptr += 4;
    if (magic != BL3D_MAGIC) return false;  // Nieprawidłowy format / Invalid format

    // Sprawdź wersję / Check version
    uint16_t version;
    std::memcpy(&version, ptr, 2); ptr += 2;
    if (version > BL3D_VERSION) return false;  // Nieobsługiwana wersja / Unsupported version

    ptr += 2; // Pomiń flagi (zarezerwowane) / Skip flags (reserved)

    // Odczytaj wymiary siatki / Read grid dimensions
    float gw, gh, gd;
    std::memcpy(&gw, ptr, 4); ptr += 4;
    std::memcpy(&gh, ptr, 4); ptr += 4;
    std::memcpy(&gd, ptr, 4); ptr += 4;

    // Odczytaj liczbę obiektów / Read object count
    uint32_t count;
    std::memcpy(&count, ptr, 4); ptr += 4;

    // Walidacja: czy bufor zawiera wystarczająco danych na wszystkie obiekty
    // Validation: does buffer contain enough data for all objects
    if (length < 24 + count * 48) return false;

    // Wyczyść bieżącą scenę i ustaw nowe wymiary siatki
    // Clear current scene and set new grid dimensions
    objects_.clear();
    gridW_ = gw; gridH_ = gh; gridD_ = gd;
    nextId_ = 1;  // Zostanie zaktualizowane / Will be updated below

    // Wczytaj obiekty / Load objects
    for (uint32_t i = 0; i < count; ++i) {
        SceneObject obj;
        std::memcpy(&obj.id, ptr, 4);          ptr += 4;
        std::memcpy(&obj.modelId, ptr, 4);      ptr += 4;
        std::memcpy(&obj.position.x, ptr, 4);   ptr += 4;
        std::memcpy(&obj.position.y, ptr, 4);   ptr += 4;
        std::memcpy(&obj.position.z, ptr, 4);   ptr += 4;
        std::memcpy(&obj.rotation.x, ptr, 4);   ptr += 4;
        std::memcpy(&obj.rotation.y, ptr, 4);   ptr += 4;
        std::memcpy(&obj.rotation.z, ptr, 4);   ptr += 4;
        std::memcpy(&obj.scale.x, ptr, 4);      ptr += 4;
        std::memcpy(&obj.scale.y, ptr, 4);      ptr += 4;
        std::memcpy(&obj.scale.z, ptr, 4);      ptr += 4;
        std::memcpy(&obj.weight, ptr, 4);        ptr += 4;

        // Aktualizuj nextId_ aby nowe obiekty miały unikalne ID
        // Update nextId_ so new objects get unique IDs
        if (obj.id >= nextId_) nextId_ = obj.id + 1;
        objects_[obj.id] = obj;
    }

    // Przebuduj octree z wczytanymi obiektami (przelicza worldAABB)
    // Rebuild octree with loaded objects (recomputes worldAABB)
    rebuildOctree();
    return true;
}

// ═══════════════════════════════════════════════════════════════════════════════
// Queries — Zapytania o stan sceny / Scene state queries
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * getObjectCount — Zwraca liczbę obiektów w scenie
 *                  Returns the number of objects in the scene
 */
int SceneEngine::getObjectCount() const {
    return static_cast<int>(objects_.size());
}

/**
 * getAllObjectIds — Zwraca listę ID wszystkich obiektów
 *                  Returns a list of all object IDs
 *
 * Rezerwuje pamięć z góry (reserve) dla wydajności.
 * Pre-allocates memory (reserve) for efficiency.
 */
std::vector<uint32_t> SceneEngine::getAllObjectIds() const {
    std::vector<uint32_t> ids;
    ids.reserve(objects_.size());  // Unikaj realokacji / Avoid reallocations
    for (auto& [id, _] : objects_) ids.push_back(id);
    return ids;
}

/**
 * getObjectData — Pobiera pełne dane transformacji obiektu
 *                 Retrieves full transform data for an object
 *
 * Używa wskaźników wyjściowych (out-params) zamiast struktury,
 * ponieważ jest wywoływane z JavaScript przez Embind i proste typy
 * są łatwiejsze do marshallowania.
 *
 * Uses output pointers (out-params) instead of struct because
 * it's called from JavaScript via Embind and primitive types are
 * easier to marshal.
 *
 * @return true jeśli obiekt istnieje i dane zostały wypełnione
 *         true if object exists and data was filled
 */
bool SceneEngine::getObjectData(
    uint32_t id,
    float* outPosX, float* outPosY, float* outPosZ,
    float* outRotX, float* outRotY, float* outRotZ,
    float* outSclX, float* outSclY, float* outSclZ,
    uint32_t* outModelId, float* outWeight) const
{
    auto it = objects_.find(id);
    if (it == objects_.end()) return false;  // Obiekt nie istnieje / Object not found

    const auto& o = it->second;
    // Wypełnij bufory wyjściowe / Fill output buffers
    *outPosX = o.position.x; *outPosY = o.position.y; *outPosZ = o.position.z;
    *outRotX = o.rotation.x; *outRotY = o.rotation.y; *outRotZ = o.rotation.z;
    *outSclX = o.scale.x;    *outSclY = o.scale.y;    *outSclZ = o.scale.z;
    *outModelId = o.modelId;
    *outWeight  = o.weight;
    return true;
}
