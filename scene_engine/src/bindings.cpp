/*******************************************************************************
 * bindings.cpp — Wiązania Emscripten Embind (C++ → JavaScript/TypeScript)
 *                Emscripten Embind bindings (C++ → JavaScript/TypeScript)
 *
 * Projekt / Project : BLACK LIGHT Collective — 3D Scene Engine
 * Autor / Author    : BLACK LIGHT Collective
 * Opis / Description:
 *   Plik definiuje wiązania (bindings) pomiędzy kodem C++ a JavaScript/TypeScript.
 *   Dzięki Emscripten Embind, klasy i struktury C++ są dostępne bezpośrednio
 *   z poziomu JS po kompilacji do WebAssembly (.wasm).
 *
 *   Defines bindings between C++ code and JavaScript/TypeScript.
 *   Thanks to Emscripten Embind, C++ classes and structs are directly
 *   accessible from JS after compilation to WebAssembly (.wasm).
 *
 *   Embind obsługuje automatyczną konwersję typów:
 *   Embind handles automatic type conversion:
 *     - Typy proste (int, float, bool) → JS number/boolean
 *       Primitive types → JS number/boolean
 *     - value_object<T> → JS plain object { field: value, ... }
 *       → JS plain object
 *     - register_vector<T> → JS array-like object z .get(i), .size(), .push_back()
 *       → JS array-like object with .get(i), .size(), .push_back()
 *     - class_<T> → JS class z metodami / JS class with methods
 *
 *   Po stronie JS / On the JS side:
 *     const engine = new Module.SceneEngine(1000, 300, 1000, 1);
 *     const id = engine.addObject(modelId, x, y, z, 0, 0, 0, 1, 1, 1, w, h, d, weight);
 *     const physics = engine.calculatePhysics();
 *     console.log(physics.balanceScore);
 ******************************************************************************/

#include "scene_engine.h"
#include <emscripten/bind.h>  // Embind — biblioteka wiązań Emscripten / Emscripten binding library

using namespace emscripten;

/**
 * EMSCRIPTEN_BINDINGS — Makro rejestrujące wiązania w module WASM
 *                        Macro registering bindings in the WASM module
 *
 * Argument "scene_engine" to unikalna nazwa modułu wiązań.
 * Blok kodu wewnątrz jest wykonywany automatycznie przy ładowaniu modułu.
 *
 * Argument "scene_engine" is the unique binding module name.
 * The code block inside is executed automatically when the module loads.
 */
EMSCRIPTEN_BINDINGS(scene_engine) {

    // ─── Vec3 ─────────────────────────────────────────────────────────────────
    // Rejestracja Vec3 jako value_object — w JS dostępny jako zwykły obiekt {x, y, z}
    // Register Vec3 as value_object — accessible in JS as plain object {x, y, z}
    //
    // Embind automatycznie konwertuje pomiędzy C++ Vec3 a JS obiektem:
    //   C++ → JS: Vec3{1.0, 2.0, 3.0} → { x: 1.0, y: 2.0, z: 3.0 }
    //   JS → C++: { x: 1.0, y: 2.0, z: 3.0 } → Vec3{1.0, 2.0, 3.0}
    value_object<Vec3>("Vec3")
        .field("x", &Vec3::x)
        .field("y", &Vec3::y)
        .field("z", &Vec3::z);

    // ─── SnapResult ───────────────────────────────────────────────────────────
    // Wynik przyciągania do siatki — prosty obiekt z 3 współrzędnymi
    // Grid snap result — simple object with 3 coordinates
    value_object<SnapResult>("SnapResult")
        .field("x", &SnapResult::x)
        .field("y", &SnapResult::y)
        .field("z", &SnapResult::z);

    // ─── CollisionResult ──────────────────────────────────────────────────────
    // Wynik detekcji kolizji — flaga + lista kolidujących ID
    // Collision detection result — flag + list of colliding IDs
    //
    // collidingIds jest typu vector<uint32_t> — wymaga rejestracji poniżej
    // collidingIds is of type vector<uint32_t> — requires registration below
    value_object<CollisionResult>("CollisionResult")
        .field("hasCollision", &CollisionResult::hasCollision)
        .field("collidingIds", &CollisionResult::collidingIds);

    // ─── PhysicsResult ────────────────────────────────────────────────────────
    // Wynik obliczeń fizycznych — waga, środek ciężkości, równowaga, stabilność, obciążenie
    // Physics calculation result — weight, center of mass, balance, stability, load
    //
    // centerOfMass jest typu Vec3 (zarejestrowany powyżej)
    // centerOfMass is of type Vec3 (registered above)
    value_object<PhysicsResult>("PhysicsResult")
        .field("totalWeight", &PhysicsResult::totalWeight)
        .field("centerOfMass", &PhysicsResult::centerOfMass)
        .field("balanceScore", &PhysicsResult::balanceScore)
        .field("isStable", &PhysicsResult::isStable)
        .field("maxLoadPerArea", &PhysicsResult::maxLoadPerArea);

    // ─── vector<uint32_t> ─────────────────────────────────────────────────────
    // Rejestracja wektora uint32_t — używany w CollisionResult.collidingIds
    // i SceneEngine.getAllObjectIds()
    // Register vector<uint32_t> — used in CollisionResult.collidingIds
    // and SceneEngine.getAllObjectIds()
    //
    // W JS dostępny jako obiekt z metodami: .get(i), .size(), .push_back(v)
    // In JS accessible as object with methods: .get(i), .size(), .push_back(v)
    register_vector<uint32_t>("VectorUint32");

    // ─── vector<uint8_t> ──────────────────────────────────────────────────────
    // Rejestracja wektora uint8_t — używany w SceneEngine.serialize()
    // Register vector<uint8_t> — used in SceneEngine.serialize()
    //
    // Pozwala na transfer binarnych danych sceny między C++ a JS
    // Enables transfer of binary scene data between C++ and JS
    register_vector<uint8_t>("VectorUint8");

    // ─── SceneEngine ──────────────────────────────────────────────────────────
    // Główna klasa silnika — wszystkie metody publiczne dostępne z JS
    // Main engine class — all public methods accessible from JS
    //
    // Przykład użycia w JS / Usage example in JS:
    //   const engine = new Module.SceneEngine(1000, 300, 1000, 1);
    //   // gridW=1000cm (10m), gridH=300cm (3m), gridD=1000cm (10m), cellSize=1cm
    class_<SceneEngine>("SceneEngine")
        // Konstruktor: (gridW, gridH, gridD, cellSize) — wszystko w cm
        // Constructor: (gridW, gridH, gridD, cellSize) — all in cm
        .constructor<float, float, float, float>()

        // --- Siatka / Grid ---
        // Przyciąganie do siatki / Grid snapping
        .function("snapToGrid", &SceneEngine::snapToGrid)
        // Sprawdzenie granic siatki / Grid boundary check
        .function("isInsideGrid", &SceneEngine::isInsideGrid)
        // Gettery wymiarów siatki / Grid dimension getters
        .function("getGridWidth", &SceneEngine::getGridWidth)
        .function("getGridHeight", &SceneEngine::getGridHeight)
        .function("getGridDepth", &SceneEngine::getGridDepth)
        .function("getCellSize", &SceneEngine::getCellSize)

        // --- Zarządzanie obiektami / Object management ---
        // Dodaj obiekt → zwraca ID / Add object → returns ID
        .function("addObject", &SceneEngine::addObject)
        // Przesuń obiekt (z snap) / Move object (with snap)
        .function("moveObject", &SceneEngine::moveObject)
        // Obróć obiekt / Rotate object
        .function("rotateObject", &SceneEngine::rotateObject)
        // Skaluj obiekt / Scale object
        .function("scaleObject", &SceneEngine::scaleObject)
        // Usuń obiekt / Remove object
        .function("removeObject", &SceneEngine::removeObject)

        // --- Detekcja kolizji / Collision detection ---
        // Kolizja danego obiektu / Collision of a specific object
        .function("checkCollision", &SceneEngine::checkCollision)
        // Kolizja w punkcie (podgląd) / Collision at point (preview)
        .function("checkCollisionAt", &SceneEngine::checkCollisionAt)

        // --- Fizyka / Physics ---
        // Obliczenia fizyczne całej sceny / Full scene physics calculation
        .function("calculatePhysics", &SceneEngine::calculatePhysics)
        // Obciążenie w punkcie / Load at point
        .function("getLoadAtPoint", &SceneEngine::getLoadAtPoint)

        // --- Serializacja / Serialization ---
        // Zapis sceny do formatu binarnego BL3D / Save scene to BL3D binary format
        // Uwaga: deserialize nie jest tu wyeksponowane — wymaga wskaźnika (pointer),
        // co nie jest bezpośrednio obsługiwane przez Embind. Deserializacja
        // jest realizowana po stronie JS z użyciem wasm memory.
        // Note: deserialize is not exposed here — it requires a raw pointer,
        // which is not directly supported by Embind. Deserialization is
        // handled on the JS side using wasm memory.
        .function("serialize", &SceneEngine::serialize)

        // --- Zapytania / Queries ---
        // Liczba obiektów w scenie / Number of objects in scene
        .function("getObjectCount", &SceneEngine::getObjectCount)
        // Lista ID wszystkich obiektów / List of all object IDs
        .function("getAllObjectIds", &SceneEngine::getAllObjectIds)
        ;

    // Uwaga: metoda getObjectData nie jest eksponowana przez Embind,
    // ponieważ używa wskaźników wyjściowych (out-params), które nie są
    // obsługiwane. Alternatywnie można by zwrócić struct lub użyć
    // val::object() do budowy obiektu JS.
    //
    // Note: getObjectData is not exposed via Embind because it uses
    // output pointers (out-params) which are not supported. Alternative
    // would be to return a struct or use val::object() to build a JS object.
}
