import client from './client';
import type { AnalysisResponse } from '../types';

export const getAnalysis = (id: string) =>
  client.get<AnalysisResponse>(`/analysis/${id}`);
