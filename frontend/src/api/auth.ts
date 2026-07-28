import client from './client';
import type { LoginRequest, RegisterRequest, TokenResponse } from '../types';

export const register = (data: RegisterRequest) =>
  client.post('/auth/register', data);

export const login = (data: LoginRequest) =>
  client.post<TokenResponse>('/auth/login', data);

export const refreshToken = (refresh_token: string) =>
  client.post<TokenResponse>('/auth/refresh', { refresh_token });
