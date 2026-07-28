export type AnalysisStatus = 'pending' | 'processing' | 'completed' | 'failed';

export interface AnalysisResponse {
  id: string;
  resume_id: string;
  status: AnalysisStatus;
  overall_score: number | null;
  ats_score: number | null;
  grammar_score: number | null;
  recruiter_score: number | null;
  summary: string | null;
  error_message: string | null;
  created_at: string;
}
