import api from './api';
import type { User, AuthTokens } from '../types';

export const authService = {
  async login(username: string, password: string): Promise<AuthTokens> {
    const { data } = await api.post<AuthTokens>('/token/', { username, password });
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    return data;
  },
  async register(payload: { username: string; email: string; password: string; password_confirm: string }): Promise<User> {
    const { data } = await api.post<User>('/accounts/register/', payload);
    return data;
  },
  async getProfile(): Promise<User> {
    const { data } = await api.get<User>('/accounts/profile/');
    return data;
  },
  async updateProfile(payload: Partial<User>): Promise<User> {
    const { data } = await api.patch<User>('/accounts/profile/', payload);
    return data;
  },
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/';
  },
  isLoggedIn: () => !!localStorage.getItem('access_token'),
};
