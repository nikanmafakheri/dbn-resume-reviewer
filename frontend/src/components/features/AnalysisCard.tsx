import type { AnalysisResponse } from '../../types';
import { ScoreGauge } from './ScoreGauge';
import { StatusBadge } from './StatusBadge';

interface AnalysisCardProps {
  analysis: AnalysisResponse;
}

export function AnalysisCard({ analysis }: AnalysisCardProps) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-900">Analysis Results</h2>
        <StatusBadge status={analysis.status} />
      </div>

      {analysis.status === 'pending' || analysis.status === 'processing' ? (
        <div className="flex flex-col items-center py-12">
          <div className="mb-4 h-12 w-12 animate-spin rounded-full border-4 border-indigo-200 border-t-indigo-600" />
          <p className="text-sm text-gray-500">Analysis in progress...</p>
          <p className="mt-1 text-xs text-gray-400">Results will appear automatically</p>
        </div>
      ) : analysis.status === 'failed' ? (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4">
          <p className="text-sm font-medium text-red-800">Analysis Failed</p>
          <p className="mt-1 text-sm text-red-600">
            {analysis.error_message || 'An unknown error occurred.'}
          </p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-2 gap-6 sm:gap-8">
            <ScoreGauge score={analysis.overall_score ?? 0} label="Overall" />
            <ScoreGauge score={analysis.ats_score ?? 0} label="ATS" />
            <ScoreGauge score={analysis.grammar_score ?? 0} label="Grammar" />
            <ScoreGauge score={analysis.recruiter_score ?? 0} label="Recruiter" />
          </div>
          {analysis.summary && (
            <div className="mt-6 rounded-lg bg-gray-50 p-4">
              <h3 className="mb-2 text-sm font-medium text-gray-700">Summary</h3>
              <p className="text-sm leading-relaxed text-gray-600">{analysis.summary}</p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
