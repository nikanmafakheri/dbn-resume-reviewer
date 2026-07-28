import { useState, useRef, type DragEvent } from 'react';
import { ALLOWED_FILE_TYPES, MAX_FILE_SIZE } from '../../utils/constants';

interface FileUploadProps {
  onFileSelected: (file: File) => void;
  isUploading?: boolean;
  error?: string | null;
}

export function FileUpload({ onFileSelected, isUploading, error }: FileUploadProps) {
  const [dragOver, setDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

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

  const handleFile = (file: File) => {
    const err = validate(file);
    if (err) {
      setValidationError(err);
      setSelectedFile(null);
      return;
    }
    setValidationError(null);
    setSelectedFile(file);
    onFileSelected(file);
  };

  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  const displayError = error || validationError;

  return (
    <div>
      <div
        className={`flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed p-10 transition-colors ${
          dragOver
            ? 'border-indigo-500 bg-indigo-50'
            : 'border-gray-300 bg-white hover:border-gray-400'
        }`}
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
      >
        {isUploading ? (
          <>
            <div className="mb-4 h-10 w-10 animate-spin rounded-full border-4 border-indigo-200 border-t-indigo-600" />
            <p className="text-sm text-gray-500">Uploading...</p>
          </>
        ) : selectedFile ? (
          <>
            <span className="mb-2 text-4xl">📄</span>
            <p className="text-sm font-medium text-gray-900">{selectedFile.name}</p>
            <p className="text-xs text-gray-500">
              {(selectedFile.size / 1024).toFixed(1)} KB
            </p>
          </>
        ) : (
          <>
            <span className="mb-4 text-4xl">📤</span>
            <p className="text-sm font-medium text-gray-900">
              Drop your resume here, or click to browse
            </p>
            <p className="mt-1 text-xs text-gray-500">
              PDF, DOC, DOCX up to 10 MB
            </p>
          </>
        )}
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.doc,.docx"
          className="hidden"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) handleFile(file);
          }}
        />
      </div>
      {displayError && (
        <p className="mt-2 text-sm text-red-600">{displayError}</p>
      )}
    </div>
  );
}
