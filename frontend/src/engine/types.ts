/**
 * BLACK LIGHT Collective — 3D Scene Engine Types
 * Shared type definitions between the TypeScript engine and future WASM bindings.
 * All spatial values are in centimeters unless otherwise noted.
 */

/** 3D vector with x, y, z components (centimeters) */
export interface Vec3 {
  x: number;
  y: number;
  z: number;
}

/** Axis-Aligned Bounding Box defined by min/max corners */
export interface AABB {
  min: Vec3;
  max: Vec3;
}

/**
 * Complete data for a single object placed in the scene.
 * Managed by the SceneEngine and mirrored in the Zustand store.
 */
export interface SceneObjectData {
  id: number;
  modelId: number;
  position: Vec3;
  rotation: Vec3;  // euler degrees
  scale: Vec3;
  bboxSize: Vec3;  // model-space size in cm
  weight: number;  // kg
  worldAABB: AABB;
}

/** Result of snapping a position to the grid */
export interface SnapResult {
  x: number;
  y: number;
  z: number;
}

/** Result of a collision query against the octree */
export interface CollisionResult {
  hasCollision: boolean;
  collidingIds: number[];
}

/**
 * Aggregated physics analysis for the entire scene.
 * Computed on-demand after object mutations.
 */
export interface PhysicsResult {
  totalWeight: number;
  centerOfMass: Vec3;
  balanceScore: number;  // 0..1, 1 = perfect
  isStable: boolean;
  maxLoadPerArea: number;  // kg per cm²
}

/**
 * Public contract for the scene engine.
 * Implemented by the TS engine; will also be implemented by the WASM module
 * so they can be swapped at runtime via dependency injection.
 */
export interface ISceneEngine {
  // ── Grid ──────────────────────────────────────────────
  snapToGrid(x: number, y: number, z: number): SnapResult;
  isInsideGrid(x: number, y: number, z: number): boolean;
  getGridWidth(): number;
  getGridHeight(): number;
  getGridDepth(): number;
  getCellSize(): number;

  // ── Object management ─────────────────────────────────
  addObject(
    modelId: number,
    posX: number, posY: number, posZ: number,
    rotX: number, rotY: number, rotZ: number,
    sclX: number, sclY: number, sclZ: number,
    bboxW: number, bboxH: number, bboxD: number,
    weight: number
  ): number;
  moveObject(id: number, x: number, y: number, z: number): boolean;
  rotateObject(id: number, rx: number, ry: number, rz: number): boolean;
  scaleObject(id: number, sx: number, sy: number, sz: number): boolean;
  removeObject(id: number): boolean;

  // ── Collision ─────────────────────────────────────────
  checkCollision(objectId: number): CollisionResult;
  checkCollisionAt(
    x: number, y: number, z: number,
    bboxW: number, bboxH: number, bboxD: number,
    excludeId: number
  ): CollisionResult;

  // ── Physics ───────────────────────────────────────────
  calculatePhysics(): PhysicsResult;
  getLoadAtPoint(x: number, y: number, z: number): number;

  // ── Serialization ─────────────────────────────────────
  serialize(): Uint8Array;
  deserialize(data: Uint8Array): boolean;

  // ── Queries ───────────────────────────────────────────
  getObjectCount(): number;
  getAllObjectIds(): number[];
  getObjectData(id: number): SceneObjectData | null;
}

// ═══════════════════════════════════════════════════════
// Django API response models
// ═══════════════════════════════════════════════════════

/** Category grouping for 3D model assets (from Django REST API) */
export interface Model3DCategory {
  id: number;
  name: string;
  slug: string;
  icon: string;
  order: number;
}

/** Single 3D model asset retrieved from the Django backend */
export interface Model3D {
  id: number;
  category: Model3DCategory;
  name: string;
  slug: string;
  description: string;
  model_file: string;  // URL
  model_file_url: string;
  thumbnail: string | null;
  bbox_width: number;
  bbox_height: number;
  bbox_depth: number;
  weight: number;
  max_instances: number;
  price_per_unit: number;
  power_consumption: number;
  is_active: boolean;
}

/** Compact scene representation used in list views */
export interface SceneListItem {
  id: number;
  name: string;
  slug: string;
  user: number | null;
  thumbnail: string | null;
  is_public: boolean;
  created_at: string;
  updated_at: string;
}

/** Full scene detail including JSON payload and grid dimensions */
export interface SceneDetail extends SceneListItem {
  description: string;
  grid_width: number;
  grid_height: number;
  grid_depth: number;
  scene_json: Record<string, unknown>;
  has_binary: boolean;
}

// ═══════════════════════════════════════════════════════
// Scene JSON format for save / load
// ═══════════════════════════════════════════════════════

/** Single object entry within a saved scene JSON */
export interface SceneJsonObject {
  id: number;
  modelId: number;
  position: Vec3;
  rotation: Vec3;
  scale: Vec3;
  bboxSize: Vec3;
  weight: number;
}

/** Top-level scene JSON structure persisted to the Django backend */
export interface SceneJson {
  version: 1;
  gridWidth: number;
  gridHeight: number;
  gridDepth: number;
  objects: SceneJsonObject[];
}
