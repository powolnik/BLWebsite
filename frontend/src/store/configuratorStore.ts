import { create } from 'zustand';
import type { SceneTemplate, ComponentCategory, SceneComponent, SceneItem } from '../types';
import { configuratorService } from '../services/configurator';
import toast from 'react-hot-toast';

interface ConfiguratorState {
  // Data from API
  templates: SceneTemplate[];
  categories: ComponentCategory[];
  isLoading: boolean;

  // Local scene state
  selectedTemplate: SceneTemplate | null;
  sceneItems: SceneItem[];
  activeCategory: string | null;

  // UI state
  step: 'build' | 'order';
  showOrderForm: boolean;

  // Actions
  fetchData: () => Promise<void>;
  selectTemplate: (t: SceneTemplate | null) => void;
  setActiveCategory: (slug: string | null) => void;
  addModule: (component: SceneComponent) => void;
  removeModule: (itemId: string) => void;
  updateQuantity: (itemId: string, qty: number) => void;
  clearScene: () => void;
  setStep: (step: 'build' | 'order') => void;
  setShowOrderForm: (show: boolean) => void;

  // Computed
  totalPrice: () => number;
  totalPower: () => number;
  totalWeight: () => number;
  itemCount: () => number;
}

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

  fetchData: async () => {
    set({ isLoading: true });
    const [templatesResult, categoriesResult] = await Promise.allSettled([
      configuratorService.getTemplates(),
      configuratorService.getCategories(),
    ]);

    const templates = templatesResult.status === 'fulfilled' ? templatesResult.value : [];
    const categories = categoriesResult.status === 'fulfilled' ? categoriesResult.value : [];

    if (templatesResult.status === 'rejected') {
      toast.error('Nie udało się załadować szablonów scen');
    }
    if (categoriesResult.status === 'rejected') {
      toast.error('Nie udało się załadować kategorii komponentów');
    }

    set({ templates, categories, isLoading: false });
    if (categories.length > 0) {
      set({ activeCategory: categories[0].slug });
    }
  },

  selectTemplate: (t) => set({ selectedTemplate: t }),
  setActiveCategory: (slug) => set({ activeCategory: slug }),

  addModule: (component) => {
    const { sceneItems } = get();
    const existing = sceneItems.find(i => i.component.id === component.id);
    if (existing) {
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

  removeModule: (itemId) => {
    set({ sceneItems: get().sceneItems.filter(i => i.id !== itemId) });
  },

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

  clearScene: () => {
    set({ sceneItems: [], selectedTemplate: null });
    toast('Scena wyczyszczona', { icon: '🗑️' });
  },

  setStep: (step) => set({ step }),
  setShowOrderForm: (show) => set({ showOrderForm: show }),

  totalPrice: () => {
    const { sceneItems, selectedTemplate } = get();
    const items = sceneItems.reduce((sum, i) => sum + parseFloat(i.component.price) * i.quantity, 0);
    const tmpl = selectedTemplate ? parseFloat(selectedTemplate.base_price) : 0;
    return items + tmpl;
  },

  totalPower: () => {
    return get().sceneItems.reduce((sum, i) => sum + i.component.power_consumption * i.quantity, 0);
  },

  totalWeight: () => {
    return get().sceneItems.reduce((sum, i) => sum + parseFloat(i.component.weight_kg) * i.quantity, 0);
  },

  itemCount: () => {
    return get().sceneItems.reduce((sum, i) => sum + i.quantity, 0);
  },
}));
