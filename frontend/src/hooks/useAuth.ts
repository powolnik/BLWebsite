import { useEffect } from 'react';
import { useAuthStore } from '../store/authStore';

export function useAuth() {
  const { user, isAuthenticated, isLoading, fetchProfile, login, logout } = useAuthStore();
  useEffect(() => { if (isAuthenticated && !user) fetchProfile(); }, [isAuthenticated, user, fetchProfile]);
  return { user, isAuthenticated, isLoading, login, logout };
}
