/**
 * BLACK LIGHT Collective — TypeScript Scene Engine
 * Pure TS port of the C++ WASM engine.
 * Implements: Octree spatial indexing, AABB collision detection,
 * physics (weight, CoM, balance, structural load), binary serialization.
 *
 * This runs identically to the C++/WASM version but in pure JS.
 * Can be swapped for WASM via the ISceneEngine interface.
 */

import type {
  Vec3, AABB, SceneObjectData, SnapResult,
  CollisionResult, PhysicsResult, ISceneEngine
} from './types';

// ─────────────── Helpers ───────────────

/** Create a Vec3 with optional defaults of 0 */
function vec3(x = 0, y = 0, z = 0): Vec3 { return { x, y, z }; }

/** Create an AABB from min/max corners */
function aabb(min: Vec3, max: Vec3): AABB { return { min, max }; }

/** Test whether two AABBs overlap on all three axes */
function aabbIntersects(a: AABB, b: AABB): boolean {
  return (a.min.x < b.max.x && a.max.x > b.min.x) &&
         (a.min.y < b.max.y && a.max.y > b.min.y) &&
         (a.min.z < b.max.z && a.max.z > b.min.z);
}

/** Return the center point of an AABB */
function aabbCenter(a: AABB): Vec3 {
  return vec3(
    (a.min.x + a.max.x) * 0.5,
    (a.min.y + a.max.y) * 0.5,
    (a.min.z + a.max.z) * 0.5
  );
}

/**
 * Compute a new AABB that encloses the original box after rotation.
 * Uses the absolute-value rotation matrix technique to find the
 * worst-case extent on each axis (Y * X * Z Euler order).
 */
function rotateAABB(halfSize: Vec3, rotation: Vec3): AABB {
  // Convert Euler degrees → radians
  const rx = rotation.x * (Math.PI / 180);
  const ry = rotation.y * (Math.PI / 180);
  const rz = rotation.z * (Math.PI / 180);

  const cy = Math.cos(ry), sy = Math.sin(ry);
  const cx = Math.cos(rx), sx = Math.sin(rx);
  const cz = Math.cos(rz), sz = Math.sin(rz);

  // Rotation matrix (Y * X * Z order)
  const m = [
    [cy*cz + sy*sx*sz,  -cy*sz + sy*sx*cz,  sy*cx],
    [cx*sz,              cx*cz,             -sx   ],
    [-sy*cz + cy*sx*sz,  sy*sz + cy*sx*cz,  cy*cx]
  ];

  // New half-extents: sum of absolute row entries × original half-sizes
  const nh = vec3(
    Math.abs(m[0][0]) * halfSize.x + Math.abs(m[0][1]) * halfSize.y + Math.abs(m[0][2]) * halfSize.z,
    Math.abs(m[1][0]) * halfSize.x + Math.abs(m[1][1]) * halfSize.y + Math.abs(m[1][2]) * halfSize.z,
    Math.abs(m[2][0]) * halfSize.x + Math.abs(m[2][1]) * halfSize.y + Math.abs(m[2][2]) * halfSize.z
  );

  return aabb(vec3(-nh.x, -nh.y, -nh.z), vec3(nh.x, nh.y, nh.z));
}

// ─────────────── Octree ───────────────

/** Maximum depth for octree subdivision */
const OCTREE_MAX_DEPTH = 10;
/** Maximum objects per leaf before subdivision */
const OCTREE_MAX_OBJECTS = 8;

/**
 * Octree node used for spatial indexing of scene objects.
 * Each node covers an axis-aligned region; when capacity is exceeded
 * the node subdivides into 8 children.
 */
class OctreeNode {
  bounds: AABB;
  depth: number;
  objectIds: number[] = [];
  children: (OctreeNode | null)[] = [null, null, null, null, null, null, null, null];
  subdivided = false;

  constructor(bounds: AABB, depth: number) {
    this.bounds = bounds;
    this.depth = depth;
  }

  /** Split this node into 8 child octants */
  subdivide(): void {
    const c = aabbCenter(this.bounds);
    const mn = this.bounds.min;
    const mx = this.bounds.max;

    // Each child gets one of the 8 octant sub-boxes
    const corners: [Vec3, Vec3][] = [
      [vec3(mn.x, mn.y, mn.z), vec3(c.x,  c.y,  c.z )],
      [vec3(c.x,  mn.y, mn.z), vec3(mx.x, c.y,  c.z )],
      [vec3(mn.x, c.y,  mn.z), vec3(c.x,  mx.y, c.z )],
      [vec3(c.x,  c.y,  mn.z), vec3(mx.x, mx.y, c.z )],
      [vec3(mn.x, mn.y, c.z ), vec3(c.x,  c.y,  mx.z)],
      [vec3(c.x,  mn.y, c.z ), vec3(mx.x, c.y,  mx.z)],
      [vec3(mn.x, c.y,  c.z ), vec3(c.x,  mx.y, mx.z)],
      [vec3(c.x,  c.y,  c.z ), vec3(mx.x, mx.y, mx.z)],
    ];

    for (let i = 0; i < 8; i++) {
      this.children[i] = new OctreeNode(aabb(corners[i][0], corners[i][1]), this.depth + 1);
    }
    this.subdivided = true;
  }

  /** Insert an object ID into this node or its children */
  insert(objId: number, objBounds: AABB): void {
    if (!aabbIntersects(this.bounds, objBounds)) return;

    // Store at this level if we haven't hit capacity or max depth
    if (!this.subdivided && (this.depth >= OCTREE_MAX_DEPTH ||
        this.objectIds.length < OCTREE_MAX_OBJECTS)) {
      this.objectIds.push(objId);
      return;
    }

    if (!this.subdivided) {
      this.subdivide();
      // Keep existing objects at this level (simplified, same as C++ version)
    }

    // Propagate into intersecting children
    for (let i = 0; i < 8; i++) {
      const child = this.children[i];
      if (child && aabbIntersects(child.bounds, objBounds)) {
        child.insert(objId, objBounds);
      }
    }
  }

  /** Collect all object IDs whose nodes intersect the query region */
  query(region: AABB, results: number[]): void {
    if (!aabbIntersects(this.bounds, region)) return;

    for (const id of this.objectIds) {
      results.push(id);
    }

    if (this.subdivided) {
      for (let i = 0; i < 8; i++) {
        this.children[i]?.query(region, results);
      }
    }
  }
}

// ─────────────── Binary Format ───────────────

/** Magic bytes "BL3D" identifying the binary scene format */
const BL3D_MAGIC = 0x424C3344;
/** Current binary format version */
const BL3D_VERSION = 1;

// ─────────────── SceneEngine ───────────────

/**
 * Pure-TypeScript implementation of the BLACK LIGHT scene engine.
 * Manages a grid-based 3D scene with octree collision detection,
 * centre-of-mass physics, and binary/JSON serialization.
 */
export class SceneEngine implements ISceneEngine {
  private gridW: number;
  private gridH: number;
  private gridD: number;
  private cellSize: number;
  private nextId = 1;
  private objects = new Map<number, SceneObjectData>();
  private octree: OctreeNode;

  /**
   * @param gridW  Grid width in cm
   * @param gridH  Grid height in cm
   * @param gridD  Grid depth in cm
   * @param cellSize  Snap resolution in cm (default 1.0 = 1 cm)
   */
  constructor(gridW: number, gridH: number, gridD: number, cellSize = 1.0) {
    this.gridW = gridW;
    this.gridH = gridH;
    this.gridD = gridD;
    this.cellSize = cellSize;
    this.octree = new OctreeNode(aabb(vec3(0, 0, 0), vec3(gridW, gridH, gridD)), 0);
  }

  // ─── Grid ───

  /** Round a single value to the nearest grid cell */
  private snap(value: number): number {
    return Math.round(value / this.cellSize) * this.cellSize;
  }

  /** Snap an (x,y,z) position to the nearest grid intersection */
  snapToGrid(x: number, y: number, z: number): SnapResult {
    return { x: this.snap(x), y: this.snap(y), z: this.snap(z) };
  }

  /** Check whether a point lies within the grid boundaries */
  isInsideGrid(x: number, y: number, z: number): boolean {
    return x >= 0 && x <= this.gridW &&
           y >= 0 && y <= this.gridH &&
           z >= 0 && z <= this.gridD;
  }

  getGridWidth(): number { return this.gridW; }
  getGridHeight(): number { return this.gridH; }
  getGridDepth(): number { return this.gridD; }
  getCellSize(): number { return this.cellSize; }

  /**
   * Resize the grid to new dimensions and rebuild the octree.
   * @param w  New width in cm
   * @param h  New height in cm
   * @param d  New depth in cm
   */
  resizeGrid(w: number, h: number, d: number): void {
    this.gridW = w;
    this.gridH = h;
    this.gridD = d;
    this.rebuildOctree();
  }

  // ─── AABB computation ───

  /**
   * Compute the world-space AABB for an object, accounting for
   * its position, scale, and rotation.
   */
  private computeWorldAABB(obj: SceneObjectData): AABB {
    // Scale the model-space half-extents
    const halfSize = vec3(
      obj.bboxSize.x * obj.scale.x * 0.5,
      obj.bboxSize.y * obj.scale.y * 0.5,
      obj.bboxSize.z * obj.scale.z * 0.5
    );

    // Expand the AABB to account for rotation
    const rotated = rotateAABB(halfSize, obj.rotation);

    // Translate to world position
    return aabb(
      vec3(obj.position.x + rotated.min.x,
           obj.position.y + rotated.min.y,
           obj.position.z + rotated.min.z),
      vec3(obj.position.x + rotated.max.x,
           obj.position.y + rotated.max.y,
           obj.position.z + rotated.max.z)
    );
  }

  /** Rebuild the octree from scratch after any spatial mutation */
  private rebuildOctree(): void {
    this.octree = new OctreeNode(
      aabb(vec3(0, 0, 0), vec3(this.gridW, this.gridH, this.gridD)), 0
    );
    for (const [id, obj] of this.objects) {
      obj.worldAABB = this.computeWorldAABB(obj);
      this.octree.insert(id, obj.worldAABB);
    }
  }

  // ─── Object Management ───

  /**
   * Add a new object to the scene and return its unique ID.
   * Position is snapped to the grid automatically.
   */
  addObject(
    modelId: number,
    posX: number, posY: number, posZ: number,
    rotX: number, rotY: number, rotZ: number,
    sclX: number, sclY: number, sclZ: number,
    bboxW: number, bboxH: number, bboxD: number,
    weight: number
  ): number {
    const obj: SceneObjectData = {
      id: this.nextId++,
      modelId,
      position: vec3(this.snap(posX), this.snap(posY), this.snap(posZ)),
      rotation: vec3(rotX, rotY, rotZ),
      scale: vec3(sclX, sclY, sclZ),
      bboxSize: vec3(bboxW, bboxH, bboxD),
      weight,
      worldAABB: aabb(vec3(), vec3())
    };
    obj.worldAABB = this.computeWorldAABB(obj);
    this.objects.set(obj.id, obj);
    this.octree.insert(obj.id, obj.worldAABB);
    return obj.id;
  }

  /** Move an object to a new (snapped) position. Returns false if ID not found. */
  moveObject(id: number, x: number, y: number, z: number): boolean {
    const obj = this.objects.get(id);
    if (!obj) return false;
    obj.position = vec3(this.snap(x), this.snap(y), this.snap(z));
    obj.worldAABB = this.computeWorldAABB(obj);
    this.rebuildOctree();
    return true;
  }

  /** Set an object's rotation (Euler degrees). Returns false if ID not found. */
  rotateObject(id: number, rx: number, ry: number, rz: number): boolean {
    const obj = this.objects.get(id);
    if (!obj) return false;
    obj.rotation = vec3(rx, ry, rz);
    obj.worldAABB = this.computeWorldAABB(obj);
    this.rebuildOctree();
    return true;
  }

  /** Set an object's scale. Returns false if ID not found. */
  scaleObject(id: number, sx: number, sy: number, sz: number): boolean {
    const obj = this.objects.get(id);
    if (!obj) return false;
    obj.scale = vec3(sx, sy, sz);
    obj.worldAABB = this.computeWorldAABB(obj);
    this.rebuildOctree();
    return true;
  }

  /** Remove an object from the scene and rebuild spatial index */
  removeObject(id: number): boolean {
    if (!this.objects.has(id)) return false;
    this.objects.delete(id);
    this.rebuildOctree();
    return true;
  }

  // ─── Collision Detection ───

  /**
   * Check whether a specific object collides with any others.
   * Uses the octree for broad-phase, then precise AABB tests.
   */
  checkCollision(objectId: number): CollisionResult {
    const result: CollisionResult = { hasCollision: false, collidingIds: [] };
    const obj = this.objects.get(objectId);
    if (!obj) return result;

    // Broad phase: gather candidate IDs from octree
    const candidates: number[] = [];
    this.octree.query(obj.worldAABB, candidates);

    // Narrow phase: precise AABB intersection, deduplicated
    const seen = new Set<number>();
    for (const cid of candidates) {
      if (cid === objectId || seen.has(cid)) continue;
      seen.add(cid);
      const cobj = this.objects.get(cid);
      if (cobj && aabbIntersects(obj.worldAABB, cobj.worldAABB)) {
        result.collidingIds.push(cid);
      }
    }

    result.hasCollision = result.collidingIds.length > 0;
    return result;
  }

  /**
   * Check for collisions at a hypothetical position/size,
   * excluding a specific object (useful during drag previews).
   */
  checkCollisionAt(
    x: number, y: number, z: number,
    bboxW: number, bboxH: number, bboxD: number,
    excludeId: number
  ): CollisionResult {
    const result: CollisionResult = { hasCollision: false, collidingIds: [] };

    // Build a test AABB at the snapped position
    const sx = this.snap(x), sy = this.snap(y), sz = this.snap(z);
    const hw = bboxW * 0.5, hh = bboxH * 0.5, hd = bboxD * 0.5;
    const testBox = aabb(
      vec3(sx - hw, sy - hh, sz - hd),
      vec3(sx + hw, sy + hh, sz + hd)
    );

    const candidates: number[] = [];
    this.octree.query(testBox, candidates);

    const seen = new Set<number>();
    for (const cid of candidates) {
      if (cid === excludeId || seen.has(cid)) continue;
      seen.add(cid);
      const cobj = this.objects.get(cid);
      if (cobj && aabbIntersects(testBox, cobj.worldAABB)) {
        result.collidingIds.push(cid);
      }
    }

    result.hasCollision = result.collidingIds.length > 0;
    return result;
  }

  // ─── Physics ───

  /**
   * Calculate aggregate physics for the entire scene:
   * total weight, centre of mass, balance score, stability flag,
   * and max load per area on the support footprint.
   */
  calculatePhysics(): PhysicsResult {
    const result: PhysicsResult = {
      totalWeight: 0,
      centerOfMass: vec3(),
      balanceScore: 1.0,
      isStable: true,
      maxLoadPerArea: 0
    };

    if (this.objects.size === 0) return result;

    let totalW = 0;
    const weightedPos = vec3();

    // Track the support footprint (objects touching the ground, y < 1cm)
    let supportMinX = this.gridW, supportMaxX = 0;
    let supportMinZ = this.gridD, supportMaxZ = 0;
    let hasSupport = false;

    for (const [, obj] of this.objects) {
      totalW += obj.weight;
      weightedPos.x += obj.position.x * obj.weight;
      weightedPos.y += obj.position.y * obj.weight;
      weightedPos.z += obj.position.z * obj.weight;

      // Ground-touching objects define the support polygon
      if (obj.worldAABB.min.y < 1.0) {
        hasSupport = true;
        supportMinX = Math.min(supportMinX, obj.worldAABB.min.x);
        supportMaxX = Math.max(supportMaxX, obj.worldAABB.max.x);
        supportMinZ = Math.min(supportMinZ, obj.worldAABB.min.z);
        supportMaxZ = Math.max(supportMaxZ, obj.worldAABB.max.z);
      }
    }

    result.totalWeight = totalW;

    // Weighted average gives centre of mass
    if (totalW > 0) {
      result.centerOfMass = vec3(
        weightedPos.x / totalW,
        weightedPos.y / totalW,
        weightedPos.z / totalW
      );
    }

    // Balance: how far CoM projects outside the support footprint
    if (hasSupport && totalW > 0) {
      const supportCX = (supportMinX + supportMaxX) * 0.5;
      const supportCZ = (supportMinZ + supportMaxZ) * 0.5;
      const supportW = supportMaxX - supportMinX;
      const supportD = supportMaxZ - supportMinZ;

      if (supportW > 0 && supportD > 0) {
        // Normalised offset from support centre (0 = centred, 1 = edge)
        const dx = Math.abs(result.centerOfMass.x - supportCX) / (supportW * 0.5);
        const dz = Math.abs(result.centerOfMass.z - supportCZ) / (supportD * 0.5);
        const dist = Math.sqrt(dx * dx + dz * dz);

        result.balanceScore = Math.max(0, 1 - dist);
        result.isStable = dx <= 1 && dz <= 1;

        // Load per area on the footprint
        const supportArea = supportW * supportD;
        if (supportArea > 0) {
          result.maxLoadPerArea = totalW / supportArea;
        }
      } else {
        // Degenerate support (line or point)
        result.balanceScore = 0.1;
        result.isStable = totalW < 5;
      }
    } else if (!hasSupport) {
      // Nothing touches the ground — fully unstable
      result.balanceScore = 0;
      result.isStable = false;
    }

    return result;
  }

  /** Sum the weight of all objects whose AABB projects above point (x, y, z) */
  getLoadAtPoint(x: number, y: number, z: number): number {
    let load = 0;
    for (const [, obj] of this.objects) {
      const bb = obj.worldAABB;
      if (x >= bb.min.x && x <= bb.max.x &&
          z >= bb.min.z && z <= bb.max.z &&
          bb.min.y >= y) {
        load += obj.weight;
      }
    }
    return load;
  }

  // ─── Serialization (BL3D binary format) ───

  /**
   * Serialize the scene to a compact binary buffer.
   * Layout: 20-byte header + 4-byte count + 48 bytes per object.
   */
  serialize(): Uint8Array {
    const objCount = this.objects.size;
    const totalSize = 20 + 4 + objCount * 48;
    const buf = new ArrayBuffer(totalSize);
    const view = new DataView(buf);
    let offset = 0;

    // Header: magic, version, flags, grid dimensions
    view.setUint32(offset, BL3D_MAGIC, true); offset += 4;
    view.setUint16(offset, BL3D_VERSION, true); offset += 2;
    view.setUint16(offset, 0, true); offset += 2; // flags (reserved)
    view.setFloat32(offset, this.gridW, true); offset += 4;
    view.setFloat32(offset, this.gridH, true); offset += 4;
    view.setFloat32(offset, this.gridD, true); offset += 4;

    // Object count
    view.setUint32(offset, objCount, true); offset += 4;

    // Per-object data: id, modelId, position, rotation, scale, weight
    for (const [, obj] of this.objects) {
      view.setUint32(offset, obj.id, true); offset += 4;
      view.setUint32(offset, obj.modelId, true); offset += 4;
      view.setFloat32(offset, obj.position.x, true); offset += 4;
      view.setFloat32(offset, obj.position.y, true); offset += 4;
      view.setFloat32(offset, obj.position.z, true); offset += 4;
      view.setFloat32(offset, obj.rotation.x, true); offset += 4;
      view.setFloat32(offset, obj.rotation.y, true); offset += 4;
      view.setFloat32(offset, obj.rotation.z, true); offset += 4;
      view.setFloat32(offset, obj.scale.x, true); offset += 4;
      view.setFloat32(offset, obj.scale.y, true); offset += 4;
      view.setFloat32(offset, obj.scale.z, true); offset += 4;
      view.setFloat32(offset, obj.weight, true); offset += 4;
    }

    return new Uint8Array(buf);
  }

  /**
   * Deserialize a BL3D binary buffer, replacing the current scene.
   * Returns false on invalid magic, unsupported version, or truncated data.
   * Note: bboxSize is NOT stored in binary and must be re-set from model data.
   */
  deserialize(data: Uint8Array): boolean {
    if (data.length < 24) return false;

    const view = new DataView(data.buffer, data.byteOffset, data.byteLength);
    let offset = 0;

    // Validate magic and version
    const magic = view.getUint32(offset, true); offset += 4;
    if (magic !== BL3D_MAGIC) return false;

    const version = view.getUint16(offset, true); offset += 2;
    if (version > BL3D_VERSION) return false;

    offset += 2; // skip flags

    // Read grid dimensions
    const gw = view.getFloat32(offset, true); offset += 4;
    const gh = view.getFloat32(offset, true); offset += 4;
    const gd = view.getFloat32(offset, true); offset += 4;

    const count = view.getUint32(offset, true); offset += 4;

    if (data.length < 24 + count * 48) return false;

    // Clear current scene and apply new grid
    this.objects.clear();
    this.gridW = gw;
    this.gridH = gh;
    this.gridD = gd;
    this.nextId = 1;

    // Read each object
    for (let i = 0; i < count; i++) {
      const id = view.getUint32(offset, true); offset += 4;
      const modelId = view.getUint32(offset, true); offset += 4;
      const px = view.getFloat32(offset, true); offset += 4;
      const py = view.getFloat32(offset, true); offset += 4;
      const pz = view.getFloat32(offset, true); offset += 4;
      const rx = view.getFloat32(offset, true); offset += 4;
      const ry = view.getFloat32(offset, true); offset += 4;
      const rz = view.getFloat32(offset, true); offset += 4;
      const sx = view.getFloat32(offset, true); offset += 4;
      const sy = view.getFloat32(offset, true); offset += 4;
      const sz = view.getFloat32(offset, true); offset += 4;
      const weight = view.getFloat32(offset, true); offset += 4;

      // Ensure nextId stays ahead of any loaded ID
      if (id >= this.nextId) this.nextId = id + 1;

      const obj: SceneObjectData = {
        id, modelId,
        position: vec3(px, py, pz),
        rotation: vec3(rx, ry, rz),
        scale: vec3(sx, sy, sz),
        bboxSize: vec3(0, 0, 0), // not stored in binary — must be re-set from model data
        weight,
        worldAABB: aabb(vec3(), vec3())
      };
      this.objects.set(id, obj);
    }

    this.rebuildOctree();
    return true;
  }

  // ─── Queries ───

  /** Return the total number of objects currently in the scene */
  getObjectCount(): number {
    return this.objects.size;
  }

  /** Return all object IDs in insertion order */
  getAllObjectIds(): number[] {
    return Array.from(this.objects.keys());
  }

  /** Retrieve a single object's data by ID (or null if not found) */
  getObjectData(id: number): SceneObjectData | null {
    return this.objects.get(id) ?? null;
  }

  // ─── JSON export (for Django API) ───

  /** Export the scene as a JSON-serializable object for the Django backend */
  toJSON(): { version: 1; gridWidth: number; gridHeight: number; gridDepth: number; objects: Array<{
    id: number; modelId: number; position: Vec3; rotation: Vec3; scale: Vec3; bboxSize: Vec3; weight: number;
  }> } {
    const objects = [];
    for (const [, obj] of this.objects) {
      objects.push({
        id: obj.id,
        modelId: obj.modelId,
        position: { ...obj.position },
        rotation: { ...obj.rotation },
        scale: { ...obj.scale },
        bboxSize: { ...obj.bboxSize },
        weight: obj.weight
      });
    }
    return {
      version: 1,
      gridWidth: this.gridW,
      gridHeight: this.gridH,
      gridDepth: this.gridD,
      objects
    };
  }

  /** Import a scene from JSON, replacing the current scene contents */
  fromJSON(json: { gridWidth?: number; gridHeight?: number; gridDepth?: number; objects: Array<{
    id?: number; modelId: number; position: Vec3; rotation: Vec3; scale: Vec3; bboxSize: Vec3; weight: number;
  }> }): void {
    this.objects.clear();
    if (json.gridWidth) this.gridW = json.gridWidth;
    if (json.gridHeight) this.gridH = json.gridHeight;
    if (json.gridDepth) this.gridD = json.gridDepth;
    this.nextId = 1;

    for (const o of json.objects) {
      this.addObject(
        o.modelId,
        o.position.x, o.position.y, o.position.z,
        o.rotation.x, o.rotation.y, o.rotation.z,
        o.scale.x, o.scale.y, o.scale.z,
        o.bboxSize.x, o.bboxSize.y, o.bboxSize.z,
        o.weight
      );
    }
  }
}
