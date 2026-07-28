import { useState } from 'react';
import { ALLOWED_FILE_TYPES, MAX_FILE_SIZE } from '../utils/constants';
import { uploadResume } from '../api/resumes';
import type { ResumeResponse } from '../types';

export function useFileUpload() {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const validate = (file: File): string | null => {
    const ext = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!ALLOWED_FILE_TYPES.includes(ext)) {
      return `Invalid file type "${ext}". Allowed: ${ALLOWED_FILE_TYPES.join(', ')}`;
    }
    if (file.size > MAX_FILE_SIZE) {
      return `File too large (${(file.size / 1024 / 1024).toFixed(1)} MB). Max: 10 MB`;
    }
    return null;
  };

  const upload = async (file: File): Promise<ResumeResponse | null> => {
    setIsUploading(true);
    setError(null);
    try {
      const { data } = await uploadResume(file);
      return data;
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Upload failed';
      setError(msg);
      return null;
    } finally {
      setIsUploading(false);
    }
  };

  return { upload, validate, isUploading, error };
}
