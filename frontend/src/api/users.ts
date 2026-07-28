import client from './client';
import type { UserResponse, UserUpdate } from '../types';

export const getMe = () => client.get<UserResponse>('/users/me');

export const updateMe = (data: UserUpdate) =>
  client.patch<UserResponse>('/users/me', data);
