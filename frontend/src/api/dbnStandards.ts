import client from './client';
import type { StandardResponse } from '../types';

export const getActiveStandard = () =>
  client.get<StandardResponse>('/dbn-standards');

export const createStandard = (data: { name: string; version: string; description?: string }) =>
  client.post<StandardResponse>('/dbn-standards', data);
