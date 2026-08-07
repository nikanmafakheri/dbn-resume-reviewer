export type ResumeStatus = 'pending' | 'processing' | 'completed' | 'failed';

export interface ResumeResponse {
  id: string;
  filename: string;
  original_filename: string;
  file_size_bytes: number | null;
  mime_type: string | null;
  status: ResumeStatus;
  created_at: string;
}
