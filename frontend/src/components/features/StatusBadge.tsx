import type { ResumeStatus, AnalysisStatus } from '../../types';

type Status = ResumeStatus | AnalysisStatus;

const config: Record<Status, { bg: string; text: string; pulse?: boolean }> = {
  pending: { bg: 'bg-yellow-100', text: 'text-yellow-800' },
  processing: { bg: 'bg-blue-100', text: 'text-blue-800', pulse: true },
  completed: { bg: 'bg-green-100', text: 'text-green-800' },
  failed: { bg: 'bg-red-100', text: 'text-red-800' },
};

export function StatusBadge({ status }: { status: Status }) {
  const c = config[status];
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
        c.bg
      } ${c.text} ${c.pulse ? 'animate-pulse' : ''}`}
    >
      {status}
    </span>
  );
}
