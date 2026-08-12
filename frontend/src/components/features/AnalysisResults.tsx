import { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../../context/LanguageContext';
import { ScoreGauge } from './ScoreGauge';
import { Button } from '../ui/Button';
import { Section } from '../ui/Section';
import { getBandKey } from '../ui/ScoreRing';
import { API_BASE_URL, isRateLimitError } from '../../lib/api';
import type { ScoreResult } from '../../types/analysis';

/** Renders a titled list of strengths / weaknesses / missing skills / recommendations. */
function InsightCard({
  title,
  items,
  empty,
  muted,
}: {
  title: string;
  items: string[];
  empty: string;
  muted?: boolean;
}) {
  return (
    <div className="card-flat anim-fade-up flex flex-col gap-3 p-6">
      <p className="text-xs font-semibold uppercase tracking-wide text-[var(--text-muted)]">
        {title}
      </p>
      {items.length === 0 ? (
        <p className="text-sm italic text-[var(--text-secondary)]">{empty}</p>
      ) : (
        <ul className="flex flex-col gap-2">
          {items.map((item) => (
            <li key={item} className="flex items-start gap-2 text-sm leading-relaxed">
              <span
                className={`mt-1 h-1.5 w-1.5 shrink-0 rounded-full ${
                  muted ? 'bg-[var(--brand)]' : 'bg-[var(--text-secondary)]'
                }`}
              />
              <span className="text-[var(--text-primary)]">{item}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

interface ScoreData {
  overall_score: number | null;
  ats_score: number | null;
  skills_score: number | null;
  experience_score: number | null;
  formatting_score: number | null;
  content_score: number | null;
  summary: string | null;
  analysis_fa: string | null;
  feedback: Record<string, unknown>;
  scores_json: ScoreResult | null;
  status: string;
  error_message: string | null;
  error_code: string | null;
}

interface AnalysisResultsProps {
  analysisId: string | null;
  onRetry: () => void;
  onReset: () => void;
}

/** Polling cadence for in-flight analyses (ms). */
const POLL_INTERVAL = 1000;

export function AnalysisResults({ analysisId, onRetry, onReset }: AnalysisResultsProps) {
  const { t } = useLanguage();
  const [data, setData] = useState<ScoreData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [retryCountdown, setRetryCountdown] = useState<number | null>(null);
  const intervalRef = useRef<number | undefined>(undefined);
  const abortRef = useRef<AbortController | null>(null);

  // Placeholder scores for the pre-analysis teaser — generated once per mount
  // so they don't jump around on each 3s poll. These are a visual preview ONLY;
  // the real, deterministic scores replace them the moment analysis completes.
  const [previewScores] = useState<number[]>(() =>
    // 5 dimensions + overall = 6 gauges, each a stable random 50–95.
    Array.from({ length: 6 }, () => 50 + Math.floor(Math.random() * 46)),
  );

  // Auto-retry after a quota countdown (e.g. 30s) so the user isn't expected
  // to stare at the page — we re-trigger the same resume once capacity frees.
  useEffect(() => {
    if (retryCountdown === null) return;
    if (retryCountdown <= 0) {
      setRetryCountdown(null);
      onRetry();
      return;
    }
    const id = window.setTimeout(() => setRetryCountdown((c) => (c === null ? null : c - 1)), 1000);
    return () => window.clearTimeout(id);
  }, [retryCountdown, onRetry]);

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
        // A rate-limited failure is a capacity pause, not a bug — offer a
        // friendly wait + auto-retry. Restart the countdown if still pending.
        const isQuota =
          json.status === 'failed' &&
          (json.error_code === 'rate_limited' ||
            isRateLimitError(null, json.error_message));
        if (isQuota) {
          setRetryCountdown((c) => (c === null || c <= 0 ? 30 : c));
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

  // Pre-analysis teaser — a lively preview dashboard while the LLM works.
  // The scores here are placeholder ONLY (random 50–95, stable per mount); they
  // are replaced by the real, deterministic scores the moment analysis lands.
  const [previewOverall, previewAts, previewSkills, previewExp, previewFmt, previewCtn] = previewScores;
  const previewGauges: { key: 'analysis.ats' | 'analysis.skills' | 'analysis.experience' | 'analysis.formatting' | 'analysis.content'; value: number }[] = [
    { key: 'analysis.ats', value: previewAts },
    { key: 'analysis.skills', value: previewSkills },
    { key: 'analysis.experience', value: previewExp },
    { key: 'analysis.formatting', value: previewFmt },
    { key: 'analysis.content', value: previewCtn },
  ];

  if (loading && !data) {
    return (
      <Section size="sm" className="max-w-4xl">
        <h2 className="anim-fade-up mb-4 text-center text-3xl font-bold tracking-tight text-[var(--text-primary)]">
          {t('analysis.overall')}
        </h2>
        <p className="anim-fade-up mb-10 text-center text-sm text-[var(--text-secondary)]" style={{ animationDelay: '60ms' }}>
          {t('analysis.processing')}
        </p>

        {/* Preview overall — same layout as the completed dashboard */}
        <div className="anim-scale-in flex justify-center">
          <ScoreGauge score={previewOverall} label={t('analysis.overall')} size={180} hint={t(getBandKey(previewOverall))} />
        </div>

        <div className="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-5">
          {previewGauges.map((g) => (
            <ScoreGauge key={g.key} score={g.value} label={t(g.key)} size={120} />
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

  // Processing / pending — offer a way out so users are never stuck. Show the
  // preview dashboard (placeholder scores) underneath so the state stays lively.
  if (data?.status === 'pending' || data?.status === 'processing') {
    return (
      <Section size="sm" className="max-w-4xl">
        <div className="card-flat mx-auto flex max-w-md flex-col items-center gap-4 p-8 text-center">
          <div className="h-9 w-9 animate-spin rounded-full border-4 border-[var(--brand)] border-t-transparent" />
          <div>
            <p className="text-sm font-semibold text-[var(--text-primary)]">{t('analysis.processing')}</p>
            <p className="mt-1 text-xs text-[var(--text-muted)]">{t('analysis.processingHint')}</p>
          </div>
          <Button variant="ghost" size="sm" onClick={onReset}>
            {t('analysis.cancel')}
          </Button>
        </div>
        <div className="mt-10 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-5">
          {previewGauges.map((g) => (
            <ScoreGauge key={g.key} score={g.value} label={t(g.key)} size={120} />
          ))}
        </div>
      </Section>
    );
  }

  // Quota / capacity pause — friendly "please wait" with an auto-retry
  // countdown. Not a bug; the resume is preserved, no re-upload needed.
  const isQuotaPause =
    data?.status === 'failed' &&
    (data.error_code === 'rate_limited' || isRateLimitError(null, data.error_message));

  if (isQuotaPause) {
    return (
      <Section size="sm" className="max-w-md text-center">
        <div className="card-flat flex flex-col items-center gap-4 p-8">
          <div className="h-9 w-9 animate-spin rounded-full border-4 border-[var(--warning)] border-t-transparent" />
          <div>
            <p className="text-sm font-semibold text-[var(--text-primary)]">{t('quota.title')}</p>
            <p className="mt-1 text-sm text-[var(--text-secondary)]">{t('quota.body')}</p>
            <p className="mt-2 text-xs text-[var(--text-muted)]">{t('quota.keepResume')}</p>
            {retryCountdown !== null && (
              <p className="mt-2 text-xs font-medium text-[var(--warning)]">
                {t('quota.waiting').replace('{seconds}', String(retryCountdown))}
              </p>
            )}
          </div>
          <Button onClick={onRetry} variant="secondary" size="sm">
            {t('quota.retryNow')}
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
  // Mirror the backend's fallback: flat scalar columns are preferred, but if
  // any is null (e.g. a legacy/half-written row) read the dimension score from
  // the nested scores_json so a gauge never silently shows 0.
  const rawDims = data?.scores_json?.dimensions;
  const dim = (key: 'ats' | 'skills' | 'experience' | 'formatting' | 'content'): number => {
    const flat = data?.[`${key}_score` as 'ats_score'];
    if (flat != null) return flat;
    const d = rawDims?.[key];
    return typeof d?.score === 'number' ? d.score : 0;
  };
  const subScores: { key: 'analysis.ats' | 'analysis.skills' | 'analysis.experience' | 'analysis.formatting' | 'analysis.content'; value: number }[] = [
    { key: 'analysis.ats', value: dim('ats') },
    { key: 'analysis.skills', value: dim('skills') },
    { key: 'analysis.experience', value: dim('experience') },
    { key: 'analysis.formatting', value: dim('formatting') },
    { key: 'analysis.content', value: dim('content') },
  ];

  const feedback = data?.feedback ?? {};
  const strengths = (feedback.strengths as string[]) ?? data?.scores_json?.strengths ?? [];
  const weaknesses = (feedback.weaknesses as string[]) ?? data?.scores_json?.weaknesses ?? [];
  const missingSkills = (feedback.missing_skills as string[]) ?? data?.scores_json?.missing_skills ?? [];
  const recommendations =
    (feedback.actionable_recommendations as string[]) ??
    data?.scores_json?.actionable_recommendations ?? [];

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
          <div key={s.key} className="flex flex-col items-center justify-center gap-3 p-6">
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

      {/* Persian professional analysis (shown in fa locale; always stored) */}
      {data?.analysis_fa && (
        <div
          className="card-flat anim-fade-up mt-12 p-7"
          style={{ animationDelay: '135ms', direction: 'rtl', textAlign: 'right' }}
        >
          <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-[var(--text-muted)]">
            {t('analysis.persianAnalysis')}
          </p>
          <p className="whitespace-pre-line text-[15px] leading-relaxed text-[var(--text-primary)]">
            {data.analysis_fa}
          </p>
        </div>
      )}

      {/* Insights */}
      <div className="stagger mt-12 grid grid-cols-1 gap-6 md:grid-cols-2">
        <InsightCard
          title={t('analysis.strengths')}
          items={strengths}
          empty={t('analysis.noStrengths')}
        />
        <InsightCard
          title={t('analysis.weaknesses')}
          items={weaknesses}
          empty={t('analysis.noWeaknesses')}
        />
        <InsightCard
          title={t('analysis.missingSkills')}
          items={missingSkills}
          empty={t('analysis.noMissingSkills')}
        />
        <InsightCard
          title={t('analysis.recommendations')}
          items={recommendations}
          empty={t('analysis.noRecommendations')}
          muted
        />
      </div>

      {/* Analyze another resume */}
      <div className="anim-fade-up mt-10 flex justify-center" style={{ animationDelay: '160ms' }}>
        <Button variant="secondary" onClick={onReset}>
          {t('analysis.analyzeAnother')}
        </Button>
      </div>
    </Section>
  );
}
