import type { ReactNode } from 'react';

type AlertVariant = 'success' | 'error' | 'warning' | 'info';

interface AlertProps {
  variant?: AlertVariant;
  children: ReactNode;
  onDismiss?: () => void;
}

const styles: Record<AlertVariant, string> = {
  success: 'bg-green-50 text-green-800 border-green-200',
  error: 'bg-red-50 text-red-800 border-red-200',
  warning: 'bg-yellow-50 text-yellow-800 border-yellow-200',
  info: 'bg-blue-50 text-blue-800 border-blue-200',
};

export function Alert({ variant = 'info', children, onDismiss }: AlertProps) {
  return (
    <div className={`flex items-start gap-2 rounded-lg border p-3 text-sm ${styles[variant]}`}>
      <div className="flex-1">{children}</div>
      {onDismiss && (
        <button onClick={onDismiss} className="text-current opacity-60 hover:opacity-100">
          &times;
        </button>
      )}
    </div>
  );
}
