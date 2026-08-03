import { useState, useEffect } from 'react';
import { useLanguage } from '../../context/LanguageContext';
import { Section } from '../ui/Section';
import { Button } from '../ui/Button';
import { Icon } from '../ui/Icon';
import { Badge } from '../ui/Badge';
import { ProgressBar } from '../ui/ProgressBar';
import { API_BASE_URL, apiGet } from '../../lib/api';

interface Criterion {
  sort_order: number;
  name: string;
  description: string | null;
  weight: number;
  max_score: number;
}

interface Standard {
  name: string;
  version: string;
  criteria: Criterion[];
}

export function StandardSection() {
  const { t } = useLanguage();
  const [standard, setStandard] = useState<Standard | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    apiGet<Standard>('/dbn-standards')
      .then((data) => setStandard(data))
      .catch(() => setError(true));
  }, []);

  const handleDownload = () => {
    const a = document.createElement('a');
    a.href = `${API_BASE_URL}/dbn-standards/template/download`;
    a.download = 'dbn-standard-resume-template.pptx';
    a.click();
  };

  return (
    <Section id="template" size="sm" className="max-w-4xl">
      <div className="card-soft p-6 sm:p-10">
        <div className="flex flex-col items-start gap-6 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-start gap-4">
            <div className="hidden h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-[var(--brand)] text-[var(--brand-contrast)] sm:flex">
              <Icon name="document" size={24} />
            </div>
            <div>
              <Badge tone="brand">{standard?.name ?? t('standard.eyebrow')}</Badge>
              <h2 className="mt-3 text-3xl font-bold tracking-tight text-[var(--text-primary)]">{t('standard.title')}</h2>
              <p className="mt-2 max-w-xl text-[15px] text-[var(--text-secondary)]">{t('standard.description')}</p>
            </div>
          </div>
          <Button size="lg" onClick={handleDownload} className="shrink-0">
            <Icon name="download" size={18} />
            {t('standard.download')}
          </Button>
        </div>

        {error && <p className="mt-6 text-sm text-[var(--danger)]">{t('standard.error')}</p>}

        {standard?.criteria && (
          <div className="mt-9 grid gap-4 sm:grid-cols-2">
            {standard.criteria.map((c) => (
              <div key={c.sort_order} className="card-flat p-5">
                <div className="flex items-center justify-between gap-3">
                  <p className="text-sm font-semibold text-[var(--text-primary)]">{c.name}</p>
                  <Badge tone="brand">{c.weight}%</Badge>
                </div>
                {c.description && (
                  <p className="mt-1 text-xs leading-relaxed text-[var(--text-muted)]">{c.description}</p>
                )}
                <div className="mt-4">
                  <ProgressBar value={c.weight} tone="gradient" size="sm" />
                </div>
              </div>
            ))}
          </div>
        )}

        {!standard && !error && (
          <div className="mt-9 grid gap-4 sm:grid-cols-2">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="card-flat p-5">
                <div className="skeleton skeleton-text w-1/3" />
                <div className="skeleton skeleton-text mt-3 w-3/4" />
                <div className="skeleton skeleton-text mt-4 w-1/2" />
              </div>
            ))}
          </div>
        )}
      </div>
    </Section>
  );
}
