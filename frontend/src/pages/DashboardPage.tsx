import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useResumes } from '../hooks/useResumes';
import { Button } from '../components/ui/Button';
import { LoadingSkeleton } from '../components/ui/LoadingSkeleton';
import { EmptyState } from '../components/ui/EmptyState';
import { ErrorState } from '../components/ui/ErrorState';
import { ResumeRow } from '../components/features/ResumeRow';

export function DashboardPage() {
  const { resumes, isLoading, error, refetch, deleteResume, triggerAnalysis } = useResumes();
  const navigate = useNavigate();
  const [analyzingIds, setAnalyzingIds] = useState<Set<string>>(new Set());

  const handleAnalyze = async (id: string) => {
    setAnalyzingIds((prev) => new Set(prev).add(id));
    try {
      const analysis = await triggerAnalysis(id);
      navigate(`/analysis/${analysis.id}`);
    } catch {
      setAnalyzingIds((prev) => {
        const next = new Set(prev);
        next.delete(id);
        return next;
      });
    }
  };

  if (isLoading) return <LoadingSkeleton rows={4} />;
  if (error) return <ErrorState message={error} onRetry={refetch} />;

  if (resumes.length === 0) {
    return (
      <EmptyState
        icon="📄"
        title="No Resumes Yet"
        description="Upload your first resume to get an AI-powered analysis of your ATS compatibility, grammar, and recruiter appeal."
        actionLabel="Upload Resume"
        onAction={() => navigate('/upload')}
      />
    );
  }

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">My Resumes</h1>
        <Button onClick={() => navigate('/upload')}>+ Upload Resume</Button>
      </div>
      <div className="space-y-3">
        {resumes.map((r) => (
          <ResumeRow
            key={r.id}
            resume={r}
            onDelete={deleteResume}
            onAnalyze={handleAnalyze}
            isAnalyzing={analyzingIds.has(r.id)}
          />
        ))}
      </div>
    </div>
  );
}
