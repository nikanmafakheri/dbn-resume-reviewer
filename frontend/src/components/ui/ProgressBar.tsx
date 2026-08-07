type ProgressTone = 'brand' | 'success' | 'warning' | 'danger' | 'gradient';

const TONES: Record<ProgressTone, string> = {
  brand: 'progress-bar',
  success: 'progress-bar progress-bar-success',
  warning: 'progress-bar progress-bar-warning',
  danger: 'progress-bar progress-bar-danger',
  gradient: 'progress-bar progress-bar-gradient',
};

interface ProgressBarProps {
  /** 0–100 */
  value: number;
  tone?: ProgressTone;
  size?: 'sm' | 'md' | 'lg';
  indeterminate?: boolean;
  className?: string;
}

export function ProgressBar({
  value,
  tone = 'brand',
  size = 'md',
  indeterminate = false,
  className = '',
}: ProgressBarProps) {
  const sizeClass = size === 'sm' ? 'progress-sm' : size === 'lg' ? 'progress-lg' : '';
  const root = ['progress', sizeClass, indeterminate ? 'progress-indeterminate' : '', className]
    .filter(Boolean)
    .join(' ');

  const clamped = Math.max(0, Math.min(100, value));

  return (
    <div className={root} role="progressbar" aria-valuenow={indeterminate ? undefined : clamped} aria-valuemin={0} aria-valuemax={100}>
      <div className={TONES[tone]} style={{ width: indeterminate ? undefined : `${clamped}%` }} />
    </div>
  );
}
