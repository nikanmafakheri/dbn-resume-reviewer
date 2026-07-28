import { createContext, useState, useEffect, useCallback, type ReactNode } from 'react';
import type { UserResponse } from '../types';
import * as authApi from '../api/auth';
import * as usersApi from '../api/users';

export interface AuthContextValue {
  user: UserResponse | null;
  accessToken: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName?: string) => Promise<void>;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserResponse | null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(() =>
    localStorage.getItem('accessToken'),
  );
  const [refreshToken, setRefreshToken] = useState<string | null>(() =>
    localStorage.getItem('refreshToken'),
  );
  const [isLoading, setIsLoading] = useState(true);

  const isAuthenticated = !!user && !!accessToken;

  // On mount, validate existing tokens
  useEffect(() => {
    const init = async () => {
      const storedAccess = localStorage.getItem('accessToken');
      const storedRefresh = localStorage.getItem('refreshToken');
      if (storedAccess && storedRefresh) {
        try {
          const { data } = await usersApi.getMe();
          setUser(data);
          setAccessToken(storedAccess);
          setRefreshToken(storedRefresh);
        } catch {
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          setAccessToken(null);
          setRefreshToken(null);
        }
      }
      setIsLoading(false);
    };
    init();
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const { data: tokens } = await authApi.login({ email, password });
    localStorage.setItem('accessToken', tokens.access_token);
    localStorage.setItem('refreshToken', tokens.refresh_token);
    setAccessToken(tokens.access_token);
    setRefreshToken(tokens.refresh_token);

    const { data: userData } = await usersApi.getMe();
    setUser(userData);
  }, []);

  const register = useCallback(
    async (email: string, password: string, fullName?: string) => {
      await authApi.register({ email, password, full_name: fullName });
      await login(email, password);
    },
    [login],
  );

  const logout = useCallback(() => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setAccessToken(null);
    setRefreshToken(null);
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{ user, accessToken, isLoading, isAuthenticated, login, register, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}
