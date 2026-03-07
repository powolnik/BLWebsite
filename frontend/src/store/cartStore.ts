import { create } from 'zustand';
import type { Cart } from '../types';
import { shopService } from '../services/shop';
import toast from 'react-hot-toast';

interface CartState {
  cart: Cart | null; isLoading: boolean;
  fetchCart: () => Promise<void>;
  addToCart: (pid: number, qty?: number) => Promise<void>;
  updateQuantity: (iid: number, qty: number) => Promise<void>;
  clearCart: () => Promise<void>;
}

export const useCartStore = create<CartState>((set) => ({
  cart: null, isLoading: false,
  fetchCart: async () => { set({ isLoading: true }); try { set({ cart: await shopService.getCart(), isLoading: false }); } catch { set({ isLoading: false }); } },
  addToCart: async (pid, qty = 1) => { try { await shopService.addToCart(pid, qty); set({ cart: await shopService.getCart() }); toast.success('Dodano do koszyka!'); } catch { toast.error('Blad dodawania'); } },
  updateQuantity: async (iid, qty) => { try { await shopService.updateCartItem(iid, qty); set({ cart: await shopService.getCart() }); } catch { toast.error('Blad aktualizacji'); } },
  clearCart: async () => { try { await shopService.clearCart(); set({ cart: null }); toast.success('Koszyk wyczyszczony'); } catch { toast.error('Blad'); } },
}));
