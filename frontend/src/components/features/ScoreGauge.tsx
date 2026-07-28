import { useEffect, useState } from 'react';

interface ScoreGaugeProps {
  score: number;
  label: string;
  size?: number;
}

function getColor(score: number): string {
  if (score < 50) return '#ef4444'; // red
  if (score < 75) return '#eab308'; // yellow
  return '#22c55e'; // green
}

export function ScoreGauge({ score, label, size = 140 }: ScoreGaugeProps) {
  const [animatedScore, setAnimatedScore] = useState(0);
  const strokeWidth = 10;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (animatedScore / 100) * circumference;
  const color = getColor(score);

  useEffect(() => {
    // Animate from 0 to actual score on mount
    const timer = setTimeout(() => setAnimatedScore(score), 100);
    return () => clearTimeout(timer);
  }, [score]);

  return (
    <div className="flex flex-col items-center">
      <svg width={size} height={size} className="transform -rotate-90">
        {/* Background track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="#e5e7eb"
          strokeWidth={strokeWidth}
        />
        {/* Foreground arc */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="transition-all duration-1000 ease-out"
        />
      </svg>
      {/* Score text overlay */}
      <div className="flex flex-col items-center -mt-20">
        <span className="text-2xl font-bold" style={{ color }}>
          {Math.round(animatedScore)}
        </span>
        <span className="text-xs text-gray-500">/ 100</span>
      </div>
      <p className="mt-2 text-sm font-medium text-gray-700">{label}</p>
    </div>
  );
}
