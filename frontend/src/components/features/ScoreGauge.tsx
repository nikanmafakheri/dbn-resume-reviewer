import { ScoreRing } from '../ui/ScoreRing';

interface ScoreGaugeProps {
  score: number;
  label: string;
  hint?: string;
  size?: number;
}

export function ScoreGauge({ score, label, hint, size = 140 }: ScoreGaugeProps) {
  return (
    <ScoreRing
      score={score}
      label={label}
      hint={hint}
      size={size}
      caption="/ 100"
    />
  );
}
