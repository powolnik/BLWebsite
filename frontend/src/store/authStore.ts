/**
 * BLACK LIGHT Collective — Authentication Store
 * Zustand store managing JWT-based auth state (login, logout, profile fetch).
 * Delegates token handling to authService.
 */

import { create } from 'zustand';
import type { User } from '../types';
import { authService } from '../services/auth';

/** Auth state shape */
interface AuthState {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;

  /** Authenticate with username/password, then fetch the user profile */
  login: (u: string, p: string) => Promise<void>;
  /** Clear tokens and reset auth state */
  logout: () => void;
  /** Fetch the current user's profile (no-op if not logged in) */
  fetchProfile: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isLoading: false,
  isAuthenticated: authService.isLoggedIn(),

  login: async (username, password) => {
    set({ isLoading: true });
    try {
      await authService.login(username, password);
      const user = await authService.getProfile();
      set({ user, isAuthenticated: true, isLoading: false });
    } catch (e) {
      set({ isLoading: false });
      throw e;
    }
  },

  logout: () => {
    authService.logout();
    set({ user: null, isAuthenticated: false });
  },

  fetchProfile: async () => {
    if (!authService.isLoggedIn()) return;
    set({ isLoading: true });
    try {
      const user = await authService.getProfile();
      set({ user, isAuthenticated: true, isLoading: false });
    } catch {
      set({ user: null, isAuthenticated: false, isLoading: false });
    }
  },
}));
