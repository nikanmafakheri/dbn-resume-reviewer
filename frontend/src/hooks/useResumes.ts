import { useState, useEffect, useCallback } from 'react';
import type { ResumeResponse } from '../types';
import * as resumesApi from '../api/resumes';

export function useResumes() {
  const [resumes, setResumes] = useState<ResumeResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchResumes = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const { data } = await resumesApi.listResumes();
      setResumes(data);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to load resumes';
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchResumes();
  }, [fetchResumes]);

  const deleteResume = async (id: string) => {
    await resumesApi.deleteResume(id);
    setResumes((prev) => prev.filter((r) => r.id !== id));
  };

  const triggerAnalysis = async (id: string) => {
    const { data } = await resumesApi.triggerAnalysis(id);
    return data;
  };

  return { resumes, isLoading, error, refetch: fetchResumes, deleteResume, triggerAnalysis };
}
