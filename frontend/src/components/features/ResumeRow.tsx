import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import type { ResumeResponse } from '../../types';
import { formatFileSize, formatDate } from '../../utils/format';
import { Button } from '../ui/Button';
import { Modal } from '../ui/Modal';
import { StatusBadge } from './StatusBadge';

interface ResumeRowProps {
  resume: ResumeResponse;
  onDelete: (id: string) => void;
  onAnalyze: (id: string) => Promise<void>;
  isAnalyzing?: boolean;
}

export function ResumeRow({ resume, onDelete, onAnalyze, isAnalyzing }: ResumeRowProps) {
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const navigate = useNavigate();

  const handleDelete = async () => {
    setDeleting(true);
    try {
      await onDelete(resume.id);
    } finally {
      setDeleting(false);
      setShowDeleteModal(false);
    }
  };

  return (
    <>
      <div className="flex items-center justify-between rounded-xl border border-gray-200 bg-white p-4 transition-colors hover:border-gray-300">
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-medium text-gray-900">
            {resume.original_filename}
          </p>
          <p className="mt-0.5 text-xs text-gray-500">
            {formatDate(resume.created_at)} &middot; {formatFileSize(resume.file_size_bytes)}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <StatusBadge status={resume.status} />
          <Button
            variant="primary"
            loading={isAnalyzing}
            onClick={() => onAnalyze(resume.id)}
            disabled={isAnalyzing}
          >
            Analyze
          </Button>
          <Button variant="danger" onClick={() => setShowDeleteModal(true)}>
            Delete
          </Button>
        </div>
      </div>

      <Modal
        open={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        title="Delete Resume"
        footer={
          <>
            <Button variant="secondary" onClick={() => setShowDeleteModal(false)}>
              Cancel
            </Button>
            <Button variant="danger" loading={deleting} onClick={handleDelete}>
              Delete
            </Button>
          </>
        }
      >
        <p>
          Are you sure you want to delete <strong>{resume.original_filename}</strong>?
          This action cannot be undone.
        </p>
      </Modal>
    </>
  );
}
