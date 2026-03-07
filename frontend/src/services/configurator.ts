import api from './api';
import type { SceneTemplate, ComponentCategory, SceneComponent, SceneOrder, OrderItem, PaginatedResponse } from '../types';

export const configuratorService = {
  getTemplates: async (): Promise<SceneTemplate[]> => {
    const { data } = await api.get('/configurator/templates/');
    return Array.isArray(data) ? data : (data as PaginatedResponse<SceneTemplate>).results;
  },
  getCategories: async (): Promise<ComponentCategory[]> => (await api.get('/configurator/categories/')).data,
  getComponents: async (categoryId?: number): Promise<PaginatedResponse<SceneComponent>> =>
    (await api.get('/configurator/components/', { params: categoryId ? { category: categoryId } : {} })).data,
  getOrders: async (): Promise<PaginatedResponse<SceneOrder>> => (await api.get('/configurator/orders/')).data,
  getOrder: async (id: number): Promise<SceneOrder> => (await api.get(`/configurator/orders/${id}/`)).data,
  createOrder: async (payload: { template?: number; event_name: string; event_date: string; event_location: string; expected_audience?: number; notes?: string }): Promise<SceneOrder> =>
    (await api.post('/configurator/orders/', payload)).data,
  addItem: async (orderId: number, componentId: number, quantity = 1): Promise<OrderItem> =>
    (await api.post(`/configurator/orders/${orderId}/add_item/`, { component_id: componentId, quantity })).data,
  removeItem: async (orderId: number, itemId: number): Promise<void> => { await api.post(`/configurator/orders/${orderId}/remove_item/`, { item_id: itemId }); },
  submitOrder: async (orderId: number) => (await api.post(`/configurator/orders/${orderId}/submit/`)).data,
  getPowerSummary: async (orderId: number) => (await api.get(`/configurator/orders/${orderId}/power_summary/`)).data,
};
