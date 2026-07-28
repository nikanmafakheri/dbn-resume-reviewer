export function LoadingSkeleton({ rows = 4 }: { rows?: number }) {
  return (
    <div className="space-y-4">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="animate-pulse rounded-xl border border-gray-100 bg-white p-4">
          <div className="mb-3 h-4 w-3/5 rounded bg-gray-200" />
          <div className="mb-2 h-3 w-2/5 rounded bg-gray-100" />
          <div className="h-3 w-1/3 rounded bg-gray-100" />
        </div>
      ))}
    </div>
  );
}
