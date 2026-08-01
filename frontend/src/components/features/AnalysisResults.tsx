import { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../../context/LanguageContext';
import { ScoreGauge } from './ScoreGauge';
import { Button } from '../ui/Button';
import { Section } from '../ui/Section';
import { getBandKey } from '../ui/ScoreRing';
import { API_BASE_URL } from '../../lib/api';

interface ScoreData {
  overall_score: number | null;
  ats_score: number | null;
  grammar_score: number | null;
  recruiter_score: number | null;
  summary: string | null;
  status: string;
  error_message: string | null;
}

interface AnalysisResultsProps {
  analysisId: string | null;
  onRetry: () => void;
  onReset: () => void;
}

/** Polling cadence for in-flight analyses (ms). */
const POLL_INTERVAL = 3000;

export function AnalysisResults({ analysisId, onRetry, onReset }: AnalysisResultsProps) {
  const { t } = useLanguage();
  const [data, setData] = useState<ScoreData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const intervalRef = useRef<number | undefined>(undefined);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    if (!analysisId) return;

    const fetchAnalysis = async () => {
      // Abort any in-flight request from a previous poll tick so we never
      // race: a slow response can't overwrite a newer one.
      abortRef.current?.abort();
      const controller = new AbortController();
      abortRef.current = controller;

      setLoading(true);
      try {
        const res = await fetch(`${API_BASE_URL}/analysis/${analysisId}`, {
          signal: controller.signal,
        });
        if (!res.ok) throw new Error('Not found');
        const json: ScoreData = await res.json();
        setData(json);
        setError(null);
        if (json.status === 'completed' || json.status === 'failed') {
          clearInterval(intervalRef.current);
        }
      } catch (err) {
        // Ignore abort noise — only surface genuine failures.
        if (err instanceof DOMException && err.name === 'AbortError') return;
        setError(err instanceof Error ? err.message : 'Failed to load');
        clearInterval(intervalRef.current);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
    intervalRef.current = window.setInterval(fetchAnalysis, POLL_INTERVAL);

    return () => {
      clearInterval(intervalRef.current);
      abortRef.current?.abort();
    };
  }, [analysisId]);

  if (!analysisId) return null;

  // Initial loading — skeleton rings with title
  if (loading && !data) {
    return (
      <Section size="sm" className="max-w-3xl">
        <div className="skeleton skeleton-title mx-auto mb-10 h-8 w-56" />
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="flex flex-col items-center gap-4">
              <div className="skeleton skeleton-circle h-[110px] w-[110px]" />
              <div className="skeleton skeleton-text w-24" />
            </div>
          ))}
        </div>
      </Section>
    );
  }

  // Error state
  if (error) {
    return (
      <Section size="sm" className="max-w-md text-center">
        <div className="card-flat flex flex-col items-center gap-4 p-8">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-[var(--danger-soft)] text-[var(--danger)]">
            <span className="text-xl">!</span>
          </div>
          <div>
            <p className="text-sm font-semibold text-[var(--text-primary)]">{t('analysis.errorTitle')}</p>
            <p className="mt-1 text-sm text-[var(--text-secondary)]">{error}</p>
          </div>
          <Button onClick={onRetry} variant="secondary" size="sm">{t('analysis.retry')}</Button>
        </div>
      </Section>
    );
  }

  // Processing / pending — offer a way out so users are never stuck
  if (data?.status === 'pending' || data?.status === 'processing') {
    return (
      <Section size="sm" className="max-w-md text-center">
        <div className="card-flat flex flex-col items-center gap-4 p-8">
          <div className="h-9 w-9 animate-spin rounded-full border-4 border-[var(--brand)] border-t-transparent" />
          <div>
            <p className="text-sm font-semibold text-[var(--text-primary)]">{t('analysis.processing')}</p>
            <p className="mt-1 text-xs text-[var(--text-muted)]">{t('analysis.processingHint')}</p>
          </div>
          <Button variant="ghost" size="sm" onClick={onReset}>
            {t('analysis.cancel')}
          </Button>
        </div>
      </Section>
    );
  }

  // Failed
  if (data?.status === 'failed') {
    return (
      <Section size="sm" className="max-w-md text-center">
        <div className="card-flat flex flex-col items-center gap-4 p-8">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-[var(--danger-soft)] text-[var(--danger)]">
            <span className="text-xl">!</span>
          </div>
          <div>
            <p className="text-sm font-semibold text-[var(--text-primary)]">{t('analysis.failed')}</p>
            {data.error_message && <p className="mt-1 text-sm text-[var(--text-secondary)]">{data.error_message}</p>}
          </div>
          <Button onClick={onRetry} variant="secondary" size="sm">{t('analysis.retry')}</Button>
        </div>
      </Section>
    );
  }

  // Completed dashboard
  const overall = data?.overall_score ?? 0;
  const subScores: { key: 'analysis.ats' | 'analysis.grammar' | 'analysis.recruiter'; value: number }[] = [
    { key: 'analysis.ats', value: data?.ats_score ?? 0 },
    { key: 'analysis.grammar', value: data?.grammar_score ?? 0 },
    { key: 'analysis.recruiter', value: data?.recruiter_score ?? 0 },
  ];

  return (
    <Section id="results" size="sm" className="max-w-4xl">
      <h2 className="anim-fade-up mb-4 text-center text-3xl font-bold tracking-tight text-[var(--text-primary)]">
        {t('analysis.completed')}
      </h2>
      <p className="anim-fade-up mb-12 text-center text-sm text-[var(--text-secondary)]" style={{ animationDelay: '60ms' }}>
        {t('analysis.subtitle')}
      </p>

      {/* Overall score — dominant, centered */}
      <div className="anim-scale-in flex justify-center">
        <ScoreGauge
          score={overall}
          label={t('analysis.overall')}
          hint={t(getBandKey(overall))}
          size={180}
        />
      </div>

      {/* Sub-scores */}
      <div className="stagger mt-12 grid grid-cols-1 gap-6 sm:grid-cols-3">
        {subScores.map((s) => (
          <div key={s.key} className="card-flat flex flex-col items-center justify-center gap-3 p-6">
            <ScoreGauge score={s.value} label={t(s.key)} hint={t(getBandKey(s.value))} size={96} />
          </div>
        ))}
      </div>

      {/* Summary */}
      {data?.summary && (
        <div className="card-flat anim-fade-up mt-12 p-7" style={{ animationDelay: '120ms' }}>
          <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-[var(--text-muted)]">
            {t('analysis.summary')}
          </p>
          <p className="text-[15px] leading-relaxed text-[var(--text-secondary)]">{data.summary}</p>
        </div>
      )}

      {/* Analyze another resume */}
      <div className="anim-fade-up mt-10 flex justify-center" style={{ animationDelay: '160ms' }}>
        <Button variant="secondary" onClick={onReset}>
          {t('analysis.analyzeAnother')}
        </Button>
      </div>
    </Section>
  );
}
