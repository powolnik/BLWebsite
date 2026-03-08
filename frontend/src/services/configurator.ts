import api from './api';
import type { SceneTemplate, ComponentCategory, SceneComponent, PaginatedResponse } from '../types';

export const configuratorService = {
  getTemplates: async (): Promise<SceneTemplate[]> => {
    const { data } = await api.get('/configurator/templates/');
    return Array.isArray(data) ? data : (data as PaginatedResponse<SceneTemplate>).results;
  },
  getCategories: async (): Promise<ComponentCategory[]> => {
    const { data } = await api.get('/configurator/categories/');
    return Array.isArray(data) ? data : data.results ?? data;
  },
  getComponents: async (): Promise<SceneComponent[]> => {
    const { data } = await api.get('/configurator/components/', { params: { page_size: 100 } });
    return Array.isArray(data) ? data : (data as PaginatedResponse<SceneComponent>).results;
  },
  submitOrder: async (payload: {
    template?: number;
    event_name: string;
    event_date: string;
    event_location: string;
    expected_audience?: number;
    notes?: string;
    scene_data?: Record<string, unknown>;
    items: { component_id: number; quantity: number }[];
  }) => {
    const { data } = await api.post('/configurator/orders/', payload);
    return data;
  },
};
