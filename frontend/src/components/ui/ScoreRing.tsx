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
  const [display, setDisplay] = useState(PREFERS_REDUCED ? Math.round(score) : 0);
  const rafRef = useRef<number | undefined>(undefined);
  // The score target for which we have already *completed* a full animation —
  // NOT the target we merely started toward. This matters for React StrictMode:
  // its mount → cancel → remount cycle re-runs this effect while the ref (and
  // the rAF) persist. If we recorded the target at animation *start*, the second
  // run would Early-return and the ring would sit frozen at 0. By recording the
  // target only once a tick has actually finished, a StrictMode re-run (or a 3s
  // poll returning the same score) can't get stuck — it simply re-animates once.
  const animatedRef = useRef<number | null>(null);

  const band = getScoreBand(score);
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;

  useEffect(() => {
    const target = Math.round(score);
    if (PREFERS_REDUCED) {
      setDisplay(target);
      animatedRef.current = target;
      return;
    }

    // Already shown this exact target — skip rather than flicker to 0. The ref
    // is only set on animation *completion*, so a StrictMode remount (which
    // cancels the rAF before any tick) still re-animates instead of freezing 0.
    if (animatedRef.current === target) return;

    setDisplay(0);
    const start = performance.now();

    const tick = (now: number) => {
      const elapsed = now - start;
      const t = Math.min(1, elapsed / DURATION);
      setDisplay(Math.round(target * easeOutCubic(t)));
      if (t >= 1) {
        animatedRef.current = target;
        rafRef.current = undefined;
        return;
      }
      rafRef.current = requestAnimationFrame(tick);
    };

    // Reset the completion ledger at the start of each new animation so a
    // cancelled rAF (StrictMode cleanup) never blocks the re-run from
    // restarting.
    animatedRef.current = null;
    rafRef.current = requestAnimationFrame(tick);
    return () => {
      if (rafRef.current !== undefined) cancelAnimationFrame(rafRef.current);
      // Leave animatedRef alone: a real unmount means the component is gone; a
      // StrictMode cancel-and-remount wants the re-run to animate, so do NOT
      // mark the target animated in cleanup.
    };
  }, [score]);

  const offset = circumference - (display / 100) * circumference;
  const shownValue = value ?? display;
  const svgLabel = ariaLabel ?? label;

  return (
    <div className={`ring ${className}`}>
      <div className="ring-svg" style={{ width: size, height: size }}>
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
