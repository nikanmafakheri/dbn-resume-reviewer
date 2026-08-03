export type AnalysisStatus = 'pending' | 'processing' | 'completed' | 'failed';

export type ScoreDimensionKey = 'ats' | 'skills' | 'experience' | 'formatting' | 'content';

export interface DimensionScore {
  score: number;
  justification: string;
}

export interface Confidence {
  label: 'low' | 'medium' | 'high';
  score: number;
  justifications_valid: number;
  note: string;
}

export interface ScoreResult {
  dimensions: Record<ScoreDimensionKey, DimensionScore>;
  overall: number;
  confidence: Confidence;
  strengths: string[];
  weaknesses: string[];
  missing_skills: string[];
  actionable_recommendations: string[];
  summary: string;
  summary_en: string;
  analysis_fa: string;
}

export interface AnalysisResponse {
  id: string;
  resume_id: string;
  status: AnalysisStatus;
  overall_score: number | null;
  ats_score: number | null;
  skills_score: number | null;
  experience_score: number | null;
  formatting_score: number | null;
  content_score: number | null;
  grammar_score: number | null;
  recruiter_score: number | null;
  summary: string | null;
  summary_en: string | null;
  analysis_fa: string | null;
  feedback: Record<string, unknown>;
  scores_json: ScoreResult | null;
  error_message: string | null;
  created_at: string;
}
