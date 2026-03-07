import api from './api';
import type { ProductCategory, ProductListItem, ProductDetail, Cart, CartItem, ShopOrder, PaginatedResponse } from '../types';

export const shopService = {
  getCategories: async (): Promise<ProductCategory[]> => (await api.get('/shop/categories/')).data,
  getProducts: async (params?: { category?: number; search?: string; ordering?: string; page?: number }): Promise<PaginatedResponse<ProductListItem>> =>
    (await api.get('/shop/products/', { params })).data,
  getProduct: async (slug: string): Promise<ProductDetail> => (await api.get(`/shop/products/${slug}/`)).data,
  getCart: async (): Promise<Cart> => (await api.get('/shop/cart/')).data,
  addToCart: async (productId: number, quantity = 1): Promise<CartItem> =>
    (await api.post('/shop/cart/', { product_id: productId, quantity })).data,
  updateCartItem: async (itemId: number, quantity: number): Promise<CartItem | null> =>
    (await api.put('/shop/cart/', { item_id: itemId, quantity })).data,
  clearCart: async (): Promise<void> => { await api.delete('/shop/cart/'); },
  checkout: async (payload: { shipping_name: string; shipping_street: string; shipping_city: string; shipping_postal_code: string; payment_provider: string; coupon_code?: string; notes?: string }): Promise<ShopOrder> =>
    (await api.post('/shop/checkout/', payload)).data,
  validateCoupon: async (code: string) => (await api.post('/shop/coupon/validate/', { code })).data,
  getOrders: async (): Promise<PaginatedResponse<ShopOrder>> => (await api.get('/shop/orders/')).data,
};
