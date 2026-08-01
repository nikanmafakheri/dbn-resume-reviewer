import { useEffect, useRef, useState } from 'react';

/** Score bands — matches design-system band tokens. */
export type ScoreBand = 'low' | 'mid' | 'good' | 'great';

export function getScoreBand(score: number): ScoreBand {
  if (score < 50) return 'low';
  if (score < 70) return 'mid';
  if (score < 85) return 'good';
  return 'great';
}

/** Human label for a band — extend keys as needed. */
export function getBandKey(score: number): 'analysis.band.low' | 'analysis.band.mid' | 'analysis.band.good' | 'analysis.band.great' {
  const band = getScoreBand(score);
  return `analysis.band.${band}`;
}

interface ScoreRingProps {
  score: number;
  /** Label shown beneath the ring. */
  label?: string;
  /** Accessible name for screen readers, e.g. "Overall score". */
  ariaLabel?: string;
  /** Caption shown inside the ring, e.g. "/ 100". */
  caption?: string;
  /** Secondary caption below the label, e.g. a band name. */
  hint?: string;
  size?: number;
  strokeWidth?: number;
  /** Optional large value; defaults to the animated score. */
  value?: number;
  className?: string;
}

const BAND_FILL: Record<ScoreBand, string> = {
  low: 'ring-fill-band-low',
  mid: 'ring-fill-band-mid',
  good: 'ring-fill-band-good',
  great: 'ring-fill-band-great',
};

const PREFERS_REDUCED =
  typeof window !== 'undefined' &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const DURATION = 900;

/** Ease-out cubic for a natural deceleration. */
function easeOutCubic(t: number): number {
  return 1 - Math.pow(1 - t, 3);
}

export function ScoreRing({
  score,
  label,
  ariaLabel,
  caption,
  hint,
  size = 140,
  strokeWidth = 10,
  value,
  className = '',
}: ScoreRingProps) {
  const [display, setDisplay] = useState(PREFERS_REDUCED ? score : 0);
  const rafRef = useRef<number | undefined>(undefined);
  const lastAnimatedRef = useRef<number | null>(null);

  const band = getScoreBand(score);
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;

  useEffect(() => {
    const target = Math.round(score);
    if (PREFERS_REDUCED) {
      setDisplay(target);
      return;
    }

    // Only re-animate when the target actually changed — otherwise every
    // poll re-render (same score) would reset the ring to 0 and make it
    // flicker on a 3s cadence.
    if (lastAnimatedRef.current === target) return;
    lastAnimatedRef.current = target;

    setDisplay(0);
    const start = performance.now();

    const tick = (now: number) => {
      const elapsed = now - start;
      const t = Math.min(1, elapsed / DURATION);
      setDisplay(Math.round(target * easeOutCubic(t)));
      if (t < 1) rafRef.current = requestAnimationFrame(tick);
    };

    rafRef.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(rafRef.current!);
  }, [score]);

  const offset = circumference - (display / 100) * circumference;
  const shownValue = value ?? display;
  const svgLabel = ariaLabel ?? label;

  return (
    <div className={`ring ${className}`} style={{ width: size, height: size }}>
      <svg
        width={size}
        height={size}
        className="block"
        role="img"
        aria-label={svgLabel ? `${svgLabel}: ${shownValue} out of 100` : undefined}
      >
        <circle
          className="ring-track"
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          strokeWidth={strokeWidth}
        />
        <circle
          className={`ring-fill ${BAND_FILL[band]}`}
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
        />
      </svg>
      <div className="ring-label" aria-hidden="true">
        <span className="ring-value" style={{ fontSize: size * 0.24 }}>
          {shownValue}
        </span>
        {caption && <span className="ring-caption">{caption}</span>}
      </div>
      {(label || hint) && (
        <div className="mt-3 text-center">
          {label && <p className="text-sm font-medium text-[var(--text-primary)]">{label}</p>}
          {hint && <p className="mt-0.5 text-xs font-medium text-[var(--text-muted)]">{hint}</p>}
        </div>
      )}
    </div>
  );
}
