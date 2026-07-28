import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FileUpload } from '../components/features/FileUpload';
import { Button } from '../components/ui/Button';
import { Alert } from '../components/ui/Alert';
import { useFileUpload } from '../hooks/useFileUpload';
import { triggerAnalysis } from '../api/resumes';

export function UploadPage() {
  const navigate = useNavigate();
  const { upload, validate, isUploading, error } = useFileUpload();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleFileSelected = (file: File) => {
    setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    const validationError = validate(selectedFile);
    if (validationError) return;

    const resume = await upload(selectedFile);
    if (resume) {
      setSuccess(`"${resume.original_filename}" uploaded successfully!`);
      // Auto-trigger analysis and navigate
      try {
        const analysis = await triggerAnalysis(resume.id);
        navigate(`/analysis/${analysis.data.id}`);
      } catch {
        navigate('/');
      }
    }
  };

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-2 text-2xl font-bold text-gray-900">Upload Resume</h1>
      <p className="mb-6 text-sm text-gray-500">
        Upload your resume in PDF, DOC, or DOCX format for instant AI analysis.
      </p>

      <FileUpload
        onFileSelected={handleFileSelected}
        isUploading={isUploading}
        error={error}
      />

      {success && (
        <Alert variant="success" className="mt-4" onDismiss={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      {selectedFile && !isUploading && (
        <div className="mt-4 flex justify-end gap-3">
          <Button variant="secondary" onClick={() => navigate('/')}>
            Cancel
          </Button>
          <Button onClick={handleUpload}>Upload &amp; Analyze</Button>
        </div>
      )}
    </div>
  );
}
