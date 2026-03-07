import { useEffect } from 'react';
import { useCartStore } from '../store/cartStore';
import { useAuthStore } from '../store/authStore';

export function useCart() {
  const { cart, isLoading, fetchCart, addToCart, updateQuantity, clearCart } = useCartStore();
  const { isAuthenticated } = useAuthStore();
  useEffect(() => { if (isAuthenticated) fetchCart(); }, [isAuthenticated, fetchCart]);
  return { cart, isLoading, addToCart, updateQuantity, clearCart };
}
