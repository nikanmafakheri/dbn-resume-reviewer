import client from './client';
import type { ResumeResponse, AnalysisResponse } from '../types';

export const uploadResume = (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return client.post<ResumeResponse>('/resumes/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const listResumes = () =>
  client.get<ResumeResponse[]>('/resumes');

export const deleteResume = (id: string) =>
  client.delete(`/resumes/${id}`);

export const triggerAnalysis = (id: string) =>
  client.post<AnalysisResponse>(`/resumes/${id}/analyze`);
