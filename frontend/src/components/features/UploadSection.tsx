import { useState, useRef } from 'react';
import { useLanguage } from '../../context/LanguageContext';
import { Button } from '../ui/Button';
import { Icon } from '../ui/Icon';
import { Section } from '../ui/Section';

interface UploadSectionProps {
  onFileSelected: (file: File) => void;
  isUploading: boolean;
  error?: string | null;
}

const ALLOWED = ['.pdf'];
const MAX_SIZE = 10 * 1024 * 1024; // 10 MB

export function UploadSection({ onFileSelected, isUploading, error }: UploadSectionProps) {
  const { t } = useLanguage();
  const [dragOver, setDragOver] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const validate = (file: File): string | null => {
    const ext = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!ALLOWED.includes(ext)) return t('upload.invalidType');
    if (file.size > MAX_SIZE) return t('upload.tooLarge');
    return null;
  };

  /**
   * Selection only previews the file — the user then explicitly
   * clicks "Upload & Analyze". This avoids uploading on drag-drop
   * and again on button click (the previous double-trigger bug).
   */
  const handleFile = (file: File) => {
    const err = validate(file);
    setValidationError(err);
    setSelectedFile(err ? null : file);
  };

  const clearFile = () => {
    setSelectedFile(null);
    setValidationError(null);
    if (inputRef.current) inputRef.current.value = '';
  };

  const displayError = error || validationError;
  // `error` may be an i18n key (e.g. quota.uploadBlocked) passed from App;
  // resolve it through t() so messages stay localized. Real Error.message
  // strings are not valid keys and pass through unchanged.
  const renderedError =
    displayError && typeof displayError === 'string' && displayError.includes('.')
      ? t(displayError as Parameters<typeof t>[0])
      : displayError;

  const dropzoneClasses = [
    'group relative flex w-full max-w-xl cursor-pointer flex-col items-center justify-center rounded-3xl border-2 border-dashed p-10 text-center outline-none transition-all duration-200 sm:p-14',
    'focus-visible:ring-2 focus-visible:ring-[rgb(var(--ring)/0.7)] focus-visible:ring-offset-2',
    dragOver
      ? 'border-[var(--brand)] bg-[var(--brand-soft)] scale-[1.01]'
      : 'border-[var(--border-strong)] bg-[var(--surface)] hover:border-[var(--brand)] hover:bg-[var(--surface-soft)]',
  ].join(' ');

  const hintId = 'upload-format-hint';

  return (
    <Section id="upload" size="sm" className="flex flex-col items-center pt-16 sm:pt-24">
      {/* Eyebrow */}
      <span className="anim-fade-up badge badge-brand">{t('upload.eyebrow')}</span>

      {/* Headline */}
      <h1 className="anim-fade-up mt-6 max-w-3xl text-center text-4xl font-extrabold leading-[1.05] tracking-tight text-[var(--text-primary)] sm:text-5xl md:text-6xl" style={{ animationDelay: '60ms' }}>
        {t('upload.headline')}{' '}
        <span className="text-gradient">{t('upload.headlineAccent')}</span>
      </h1>

      {/* Subcopy */}
      <p className="anim-fade-up mt-5 max-w-xl text-center text-base text-[var(--text-secondary)] sm:text-lg" style={{ animationDelay: '120ms' }}>
        {t('upload.description')}
      </p>

      {/*
        Dropzone as a native <label> — clicking/keyboarding activates the
        hidden file input for free, and screen readers announce the control
        as a labelled file input rather than a synthetic button.
      */}
      <label
        className={`${dropzoneClasses} anim-scale-in mt-10`}
        style={{ animationDelay: '180ms' }}
        aria-describedby={hintId}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={(e) => { e.preventDefault(); setDragOver(false); if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]); }}
      >
        {isUploading ? (
          <>
            <div className="mb-5 h-10 w-10 animate-spin rounded-full border-4 border-[var(--brand)] border-t-transparent" />
            <p className="text-sm font-medium text-[var(--text-secondary)]">{t('upload.uploading')}</p>
          </>
        ) : selectedFile ? (
          <>
            <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-[var(--brand-soft)] text-[var(--brand)]">
              <Icon name="file" size={28} />
            </div>
            <p className="max-w-full truncate text-sm font-semibold text-[var(--text-primary)]">{selectedFile.name}</p>
            <p className="mt-1 text-xs text-[var(--text-muted)]">{(selectedFile.size / 1024).toFixed(1)} KB</p>
          </>
        ) : (
          <>
            <div className="mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-[var(--brand-soft)] text-[var(--brand)] transition-transform duration-200 group-hover:scale-105">
              <Icon name="upload" size={26} />
            </div>
            <p className="text-base font-semibold text-[var(--text-primary)]">{t('upload.dragText')}</p>
            <p className="mt-1 text-sm text-[var(--text-muted)]">{t('upload.clickText')}</p>
          </>
        )}
        <input
          ref={inputRef}
          type="file"
          accept={ALLOWED.join(',')}
          className="hidden"
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) handleFile(f);
            e.target.value = '';
          }}
        />
      </label>

      {/* Format hint for screen readers */}
      <p id={hintId} className="sr-only">
        {ALLOWED.join(', ')}
      </p>

      {/* Validation / upload error */}
      {renderedError && (
        <p className="anim-fade-in mt-4 flex items-center gap-2 text-sm font-medium text-[var(--danger)]" role="alert">
          <Icon name="close" size={14} />
          {renderedError}
        </p>
      )}

      {/* CTA — uploads on explicit click only */}
      {selectedFile && !isUploading && (
        <div className="anim-fade-up mt-8 flex flex-col items-center gap-4 sm:flex-row">
          <Button size="lg" onClick={() => onFileSelected(selectedFile)}>
            <Icon name="sparkles" size={18} />
            {t('upload.button')}
          </Button>
          <Button variant="ghost" onClick={clearFile} aria-label={t('upload.clear')}>
            <Icon name="close" size={16} />
            {t('upload.clear')}
          </Button>
        </div>
      )}

      {/* Trust line */}
      {!selectedFile && !isUploading && (
        <p className="anim-fade-up mt-6 text-xs text-[var(--text-muted)]" style={{ animationDelay: '240ms' }}>
          {t('upload.trust')}
        </p>
      )}
    </Section>
  );
}
