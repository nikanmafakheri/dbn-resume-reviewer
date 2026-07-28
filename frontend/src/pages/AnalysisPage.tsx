import { useParams, Link } from 'react-router-dom';
import { useAnalysis } from '../hooks/useAnalysis';
import { AnalysisCard } from '../components/features/AnalysisCard';
import { LoadingSkeleton } from '../components/ui/LoadingSkeleton';
import { ErrorState } from '../components/ui/ErrorState';
import { Button } from '../components/ui/Button';

export function AnalysisPage() {
  const { id } = useParams<{ id: string }>();
  const { analysis, isLoading, error } = useAnalysis(id);

  if (isLoading) {
    return (
      <div>
        <div className="mb-6">
          <Link to="/" className="text-sm text-indigo-600 hover:text-indigo-500">
            &larr; Back to Dashboard
          </Link>
        </div>
        <div className="grid grid-cols-2 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="animate-pulse rounded-xl border border-gray-200 bg-white p-8">
              <div className="mx-auto h-32 w-32 rounded-full bg-gray-200" />
              <div className="mx-auto mt-4 h-4 w-20 rounded bg-gray-200" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error || !analysis) {
    return (
      <div>
        <div className="mb-6">
          <Link to="/" className="text-sm text-indigo-600 hover:text-indigo-500">
            &larr; Back to Dashboard
          </Link>
        </div>
        <ErrorState message={error || 'Analysis not found'} />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl">
      <div className="mb-6 flex items-center justify-between">
        <Link to="/" className="text-sm text-indigo-600 hover:text-indigo-500">
          &larr; Back to Dashboard
        </Link>
      </div>
      <AnalysisCard analysis={analysis} />
    </div>
  );
}
