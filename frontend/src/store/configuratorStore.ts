/**
 * BLACK LIGHT Collective — Configurator Store
 * Zustand store for the scene configurator page.
 * Manages template selection, component (module) picking, quantity tracking,
 * and computed totals (price, power, weight).
 */

import { create } from 'zustand';
import type { SceneTemplate, ComponentCategory, SceneComponent, SceneItem } from '../types';
import { configuratorService } from '../services/configurator';
import toast from 'react-hot-toast';

/** Full configurator state shape */
interface ConfiguratorState {
  // ── Data from API ──────────────────────────────────
  templates: SceneTemplate[];
  categories: ComponentCategory[];
  isLoading: boolean;

  // ── Local scene state ──────────────────────────────
  selectedTemplate: SceneTemplate | null;
  sceneItems: SceneItem[];
  activeCategory: string | null;

  // ── UI state ───────────────────────────────────────
  step: 'build' | 'order';
  showOrderForm: boolean;

  // ── Actions ────────────────────────────────────────
  fetchData: () => Promise<void>;
  selectTemplate: (t: SceneTemplate | null) => void;
  setActiveCategory: (slug: string | null) => void;
  addModule: (component: SceneComponent) => void;
  removeModule: (itemId: string) => void;
  updateQuantity: (itemId: string, qty: number) => void;
  clearScene: () => void;
  setStep: (step: 'build' | 'order') => void;
  setShowOrderForm: (show: boolean) => void;

  // ── Computed selectors ─────────────────────────────
  totalPrice: () => number;
  totalPower: () => number;
  totalWeight: () => number;
  itemCount: () => number;
}

/** Auto-incrementing ID for locally created scene items */
let idCounter = 0;

export const useConfiguratorStore = create<ConfiguratorState>((set, get) => ({
  templates: [],
  categories: [],
  isLoading: false,
  selectedTemplate: null,
  sceneItems: [],
  activeCategory: null,
  step: 'build',
  showOrderForm: false,

  /** Fetch templates and component categories from the API in parallel */
  fetchData: async () => {
    set({ isLoading: true });
    try {
      const [templates, categories] = await Promise.all([
        configuratorService.getTemplates(),
        configuratorService.getCategories(),
      ]);
      set({ templates, categories, isLoading: false });
      // Auto-select the first category tab
      if (categories.length > 0) {
        set({ activeCategory: categories[0].slug });
      }
    } catch {
      set({ isLoading: false });
      toast.error('Nie udało się załadować danych konfiguratora');
    }
  },

  selectTemplate: (t) => set({ selectedTemplate: t }),
  setActiveCategory: (slug) => set({ activeCategory: slug }),

  /**
   * Add a component to the scene.
   * If the same component already exists, increment its quantity
   * (clamped to max_quantity). Otherwise add a new SceneItem.
   */
  addModule: (component) => {
    const { sceneItems } = get();
    const existing = sceneItems.find(i => i.component.id === component.id);
    if (existing) {
      // Enforce per-component maximum
      if (existing.quantity >= component.max_quantity) {
        toast.error(`Maks. ${component.max_quantity} szt. ${component.name}`);
        return;
      }
      set({
        sceneItems: sceneItems.map(i =>
          i.id === existing.id ? { ...i, quantity: i.quantity + 1 } : i
        ),
      });
    } else {
      set({
        sceneItems: [...sceneItems, {
          id: `item-${++idCounter}`,
          component,
          quantity: 1,
        }],
      });
    }
    toast.success(`${component.name} dodany!`, { duration: 1500 });
  },

  /** Remove a scene item by its local ID */
  removeModule: (itemId) => {
    set({ sceneItems: get().sceneItems.filter(i => i.id !== itemId) });
  },

  /** Update item quantity; removes the item if qty ≤ 0 */
  updateQuantity: (itemId, qty) => {
    if (qty <= 0) {
      get().removeModule(itemId);
      return;
    }
    set({
      sceneItems: get().sceneItems.map(i =>
        i.id === itemId ? { ...i, quantity: Math.min(qty, i.component.max_quantity) } : i
      ),
    });
  },

  /** Clear all scene items and deselect the template */
  clearScene: () => {
    set({ sceneItems: [], selectedTemplate: null });
    toast('Scena wyczyszczona', { icon: '🗑️' });
  },

  setStep: (step) => set({ step }),
  setShowOrderForm: (show) => set({ showOrderForm: show }),

  // ── Computed helpers (called as functions, not selectors) ──

  /** Sum of all item prices + template base price */
  totalPrice: () => {
    const { sceneItems, selectedTemplate } = get();
    const items = sceneItems.reduce((sum, i) => sum + parseFloat(i.component.price) * i.quantity, 0);
    const tmpl = selectedTemplate ? parseFloat(selectedTemplate.base_price) : 0;
    return items + tmpl;
  },

  /** Total power consumption in watts */
  totalPower: () => {
    return get().sceneItems.reduce((sum, i) => sum + i.component.power_consumption * i.quantity, 0);
  },

  /** Total weight in kg */
  totalWeight: () => {
    return get().sceneItems.reduce((sum, i) => sum + parseFloat(i.component.weight_kg) * i.quantity, 0);
  },

  /** Total number of individual items (sum of quantities) */
  itemCount: () => {
    return get().sceneItems.reduce((sum, i) => sum + i.quantity, 0);
  },
}));
