import { create } from 'zustand';
import type { SceneTemplate, ComponentCategory, SceneOrder } from '../types';
import { configuratorService } from '../services/configurator';
import toast from 'react-hot-toast';

interface ConfiguratorState {
  templates: SceneTemplate[]; categories: ComponentCategory[]; currentOrder: SceneOrder | null;
  step: number; isLoading: boolean;
  fetchTemplates: () => Promise<void>; fetchCategories: () => Promise<void>;
  createOrder: (d: { template?: number; event_name: string; event_date: string; event_location: string }) => Promise<void>;
  addItem: (cid: number, qty?: number) => Promise<void>;
  removeItem: (iid: number) => Promise<void>;
  submitOrder: () => Promise<void>;
  setStep: (s: number) => void; reset: () => void;
}

export const useConfiguratorStore = create<ConfiguratorState>((set, get) => ({
  templates: [], categories: [], currentOrder: null, step: 0, isLoading: false,
  fetchTemplates: async () => set({ templates: await configuratorService.getTemplates() }),
  fetchCategories: async () => set({ categories: await configuratorService.getCategories() }),
  createOrder: async (data) => {
    set({ isLoading: true });
    try { const order = await configuratorService.createOrder(data); set({ currentOrder: order, step: 1, isLoading: false }); toast.success('Konfiguracja rozpoczeta!'); }
    catch { set({ isLoading: false }); toast.error('Blad tworzenia'); }
  },
  addItem: async (cid, qty = 1) => {
    const { currentOrder } = get(); if (!currentOrder) return;
    try { await configuratorService.addItem(currentOrder.id, cid, qty); set({ currentOrder: await configuratorService.getOrder(currentOrder.id) }); toast.success('Dodano!'); }
    catch { toast.error('Blad dodawania'); }
  },
  removeItem: async (iid) => {
    const { currentOrder } = get(); if (!currentOrder) return;
    try { await configuratorService.removeItem(currentOrder.id, iid); set({ currentOrder: await configuratorService.getOrder(currentOrder.id) }); }
    catch { toast.error('Blad usuwania'); }
  },
  submitOrder: async () => {
    const { currentOrder } = get(); if (!currentOrder) return;
    set({ isLoading: true });
    try { await configuratorService.submitOrder(currentOrder.id); set({ currentOrder: await configuratorService.getOrder(currentOrder.id), isLoading: false }); toast.success('Zamowienie zlozone!'); }
    catch { set({ isLoading: false }); toast.error('Blad skladania'); }
  },
  setStep: (step) => set({ step }),
  reset: () => set({ currentOrder: null, step: 0 }),
}));
