/**
 * BLACK LIGHT Collective — Axios API Client
 * Pre-configured Axios instance for all Django REST API calls.
 *
 * Features:
 *   - Auto-attaches JWT access token from localStorage on every request
 *   - Auto-refreshes expired tokens using the refresh token
 *   - Redirects to /login on unrecoverable 401 errors
 *
 * Usage: import api from './api'; api.get('/endpoint/');
 */

import axios from 'axios';

/** Create an Axios instance with the Django API base URL */
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: { 'Content-Type': 'application/json' },
});

// ── Request interceptor: attach Bearer token ────────────

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// ── Response interceptor: auto-refresh expired JWTs ─────

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const orig = err.config;

    // Only attempt refresh once per failed request (prevent infinite loops)
    if (err.response?.status === 401 && !orig._retry) {
      orig._retry = true;
      const refresh = localStorage.getItem('refresh_token');
      if (refresh) {
        try {
          // Request a new access token using the refresh token
          const { data } = await axios.post(`${api.defaults.baseURL}/token/refresh/`, { refresh });
          localStorage.setItem('access_token', data.access);
          // Retry the original request with the new token
          orig.headers.Authorization = `Bearer ${data.access}`;
          return api(orig);
        } catch {
          // Refresh failed — clear tokens and redirect to login
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(err);
  },
);

export default api;
