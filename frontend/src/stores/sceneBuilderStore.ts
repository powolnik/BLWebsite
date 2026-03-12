/**
 * BLACK LIGHT Collective — Scene Builder Zustand Store
 * Central state management for the 3D Scene Builder page.
 * Bridges the SceneEngine (spatial logic) with React components via Zustand.
 *
 * Pattern: every mutation goes through the engine first, then the
 * resulting SceneObjectData is copied into a new Map to trigger React re-renders.
 */

import { create } from 'zustand';
import { SceneEngine } from '../engine/SceneEngine';
import type { Model3D, SceneObjectData, PhysicsResult } from '../engine/types';

/** Active transform gizmo mode */
type TransformMode = 'translate' | 'rotate' | 'scale';

/** Full state shape for the scene builder */
interface SceneBuilderState {
  // ── Engine ─────────────────────────────────────────
  engine: SceneEngine;

  // ── Scene state ────────────────────────────────────
  sceneObjects: Map<number, SceneObjectData>;
  selectedObjectId: number | null;
  hoveredObjectId: number | null;
  collisions: Map<number, number[]>; // objectId → colliding ids
  physics: PhysicsResult;

  // ── UI state ───────────────────────────────────────
  transformMode: TransformMode;
  showGrid: boolean;
  showCollisions: boolean;
  showPhysics: boolean;
  gridCellDisplay: number; // visual grid cell size in cm (e.g., 10, 50, 100)

  // ── Drag state ─────────────────────────────────────
  isDragging: boolean;
  dragObjectId: number | null;

  // ── Grid shape ─────────────────────────────────────
  gridShape: 'square' | 'circle' | 'rectangle';

  // ── Available models from API ──────────────────────
  availableModels: Model3D[];

  // ── Actions ────────────────────────────────────────
  setAvailableModels: (models: Model3D[]) => void;
  addModelToScene: (model: Model3D, x: number, y: number, z: number) => number;
  moveSceneObject: (id: number, x: number, y: number, z: number) => void;
  rotateSceneObject: (id: number, rx: number, ry: number, rz: number) => void;
  scaleSceneObject: (id: number, sx: number, sy: number, sz: number) => void;
  removeSceneObject: (id: number) => void;
  selectObject: (id: number | null) => void;
  setHoveredObject: (id: number | null) => void;
  setTransformMode: (mode: TransformMode) => void;
  toggleGrid: () => void;
  toggleCollisions: () => void;
  togglePhysics: () => void;
  setGridCellDisplay: (size: number) => void;
  refreshPhysics: () => void;
  refreshCollisions: () => void;
  clearScene: () => void;
  getSceneJSON: () => object;
  loadSceneJSON: (json: any) => void;
  setDragging: (isDragging: boolean, objectId?: number | null) => void;
  setGridShape: (shape: 'square' | 'circle' | 'rectangle') => void;
  resizeGrid: (w: number, h: number, d: number) => void;
}

/**
 * Zustand store for the Scene Builder.
 * Default grid: 20 m × 10 m × 20 m at 1 cm resolution.
 */
export const useSceneBuilderStore = create<SceneBuilderState>((set, get) => ({
  engine: new SceneEngine(2000, 1000, 2000, 1.0), // 20m × 10m × 20m, 1cm grid
  sceneObjects: new Map(),
  selectedObjectId: null,
  hoveredObjectId: null,
  collisions: new Map(),
  physics: { totalWeight: 0, centerOfMass: { x: 0, y: 0, z: 0 }, balanceScore: 1, isStable: true, maxLoadPerArea: 0 },
  transformMode: 'translate',
  showGrid: true,
  showCollisions: true,
  showPhysics: true,
  gridCellDisplay: 100, // show grid lines every 1 m by default
  availableModels: [],
  isDragging: false,
  dragObjectId: null,
  gridShape: 'rectangle',

  /** Replace the full model catalogue (called after API fetch) */
  setAvailableModels: (models) => set({ availableModels: models }),

  /**
   * Place a new model in the scene at (x, y, z) cm.
   * Automatically selects the new object and refreshes physics/collisions.
   */
  addModelToScene: (model, x, y, z) => {
    const { engine } = get();
    const id = engine.addObject(
      model.id,
      x, y, z,
      0, 0, 0,          // no rotation
      1, 1, 1,           // unit scale
      model.bbox_width, model.bbox_height, model.bbox_depth,
      model.weight
    );
    const objData = engine.getObjectData(id);
    if (objData) {
      // Clone Map to trigger Zustand shallow-compare re-render
      const newMap = new Map(get().sceneObjects);
      newMap.set(id, objData);
      set({ sceneObjects: newMap, selectedObjectId: id });
      get().refreshPhysics();
      get().refreshCollisions();
    }
    return id;
  },

  /** Move an existing object and refresh derived state */
  moveSceneObject: (id, x, y, z) => {
    const { engine } = get();
    engine.moveObject(id, x, y, z);
    const objData = engine.getObjectData(id);
    if (objData) {
      const newMap = new Map(get().sceneObjects);
      newMap.set(id, objData);
      set({ sceneObjects: newMap });
      get().refreshPhysics();
      get().refreshCollisions();
    }
  },

  /** Rotate an existing object (Euler degrees) and refresh derived state */
  rotateSceneObject: (id, rx, ry, rz) => {
    const { engine } = get();
    engine.rotateObject(id, rx, ry, rz);
    const objData = engine.getObjectData(id);
    if (objData) {
      const newMap = new Map(get().sceneObjects);
      newMap.set(id, objData);
      set({ sceneObjects: newMap });
      get().refreshPhysics();
      get().refreshCollisions();
    }
  },

  /** Scale an existing object and refresh derived state */
  scaleSceneObject: (id, sx, sy, sz) => {
    const { engine } = get();
    engine.scaleObject(id, sx, sy, sz);
    const objData = engine.getObjectData(id);
    if (objData) {
      const newMap = new Map(get().sceneObjects);
      newMap.set(id, objData);
      set({ sceneObjects: newMap });
      get().refreshPhysics();
      get().refreshCollisions();
    }
  },

  /** Remove an object; deselect it if it was selected */
  removeSceneObject: (id) => {
    const { engine, selectedObjectId } = get();
    engine.removeObject(id);
    const newMap = new Map(get().sceneObjects);
    newMap.delete(id);
    set({
      sceneObjects: newMap,
      selectedObjectId: selectedObjectId === id ? null : selectedObjectId
    });
    get().refreshPhysics();
    get().refreshCollisions();
  },

  // ── Simple setters ────────────────────────────────
  selectObject: (id) => set({ selectedObjectId: id }),
  setHoveredObject: (id) => set({ hoveredObjectId: id }),
  setTransformMode: (mode) => set({ transformMode: mode }),
  toggleGrid: () => set((s) => ({ showGrid: !s.showGrid })),
  toggleCollisions: () => set((s) => ({ showCollisions: !s.showCollisions })),
  togglePhysics: () => set((s) => ({ showPhysics: !s.showPhysics })),
  setGridCellDisplay: (size) => set({ gridCellDisplay: size }),

  /** Re-run the engine's physics calculation and store the result */
  refreshPhysics: () => {
    const { engine } = get();
    set({ physics: engine.calculatePhysics() });
  },

  /** Re-check collisions for every object and store the collision map */
  refreshCollisions: () => {
    const { engine } = get();
    const collisions = new Map<number, number[]>();
    for (const id of engine.getAllObjectIds()) {
      const result = engine.checkCollision(id);
      if (result.hasCollision) {
        collisions.set(id, result.collidingIds);
      }
    }
    set({ collisions });
  },

  /** Reset the entire scene to a fresh empty state */
  clearScene: () => {
    set({
      engine: new SceneEngine(2000, 1000, 2000, 1.0),
      sceneObjects: new Map(),
      selectedObjectId: null,
      collisions: new Map(),
      physics: { totalWeight: 0, centerOfMass: { x: 0, y: 0, z: 0 }, balanceScore: 1, isStable: true, maxLoadPerArea: 0 },
      gridShape: 'rectangle',
    });
  },

  /** Export the current scene as a JSON object for the Django API */
  getSceneJSON: () => {
    return get().engine.toJSON();
  },

  /** Import a scene from JSON, replacing all current objects */
  loadSceneJSON: (json) => {
    const { engine } = get();
    engine.fromJSON(json);
    // Rebuild the React-side sceneObjects Map from the engine
    const newMap = new Map<number, SceneObjectData>();
    for (const id of engine.getAllObjectIds()) {
      const data = engine.getObjectData(id);
      if (data) newMap.set(id, data);
    }
    set({ sceneObjects: newMap, selectedObjectId: null });
    get().refreshPhysics();
    get().refreshCollisions();
  },

  /** Set drag state */
  setDragging: (isDragging, objectId) => {
    set({ isDragging, dragObjectId: objectId ?? null });
  },

  /** Set grid shape */
  setGridShape: (shape) => {
    set({ gridShape: shape });
  },

  /** Resize the grid (dimensions in metres, converted to cm for engine) */
  resizeGrid: (w, h, d) => {
    const { engine } = get();
    engine.resizeGrid(w * 100, h * 100, d * 100);

    // Rebuild sceneObjects map from engine
    const newMap = new Map<number, SceneObjectData>();
    for (const id of engine.getAllObjectIds()) {
      const data = engine.getObjectData(id);
      if (data) newMap.set(id, data);
    }

    set({ sceneObjects: newMap });
    get().refreshPhysics();
    get().refreshCollisions();
  },
}));
