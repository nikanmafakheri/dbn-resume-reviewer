import { useState, useEffect, useRef } from 'react';
import type { AnalysisResponse } from '../types';
import { getAnalysis } from '../api/analysis';

export function useAnalysis(analysisId: string | undefined) {
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const intervalRef = useRef<number | undefined>(undefined);

  useEffect(() => {
    if (!analysisId) {
      setIsLoading(false);
      return;
    }

    let cancelled = false;

    const fetch = async () => {
      try {
        const { data } = await getAnalysis(analysisId);
        if (cancelled) return;
        setAnalysis(data);
        setError(null);

        // Stop polling on terminal states
        if (data.status === 'completed' || data.status === 'failed') {
          clearInterval(intervalRef.current);
        }
      } catch (err: unknown) {
        if (cancelled) return;
        const msg = err instanceof Error ? err.message : 'Failed to fetch analysis';
        setError(msg);
        clearInterval(intervalRef.current);
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    };

    fetch();
    intervalRef.current = window.setInterval(fetch, 3000);

    return () => {
      cancelled = true;
      clearInterval(intervalRef.current);
    };
  }, [analysisId]);

  return { analysis, isLoading, error };
}
