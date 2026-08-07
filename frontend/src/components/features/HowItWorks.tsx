import { useLanguage } from '../../context/LanguageContext';
import { Section, SectionHeading } from '../ui/Section';
import { Icon } from '../ui/Icon';
import type { IconName } from '../ui/Icon';

const STEPS: {
  icon: IconName;
  num: number;
  titleKey: 'how.step1.title' | 'how.step2.title' | 'how.step3.title';
  descKey: 'how.step1.description' | 'how.step2.description' | 'how.step3.description';
}[] = [
  { icon: 'upload', num: 1, titleKey: 'how.step1.title', descKey: 'how.step1.description' },
  { icon: 'sparkles', num: 2, titleKey: 'how.step2.title', descKey: 'how.step2.description' },
  { icon: 'trending', num: 3, titleKey: 'how.step3.title', descKey: 'how.step3.description' },
];

export function HowItWorks() {
  const { t } = useLanguage();

  return (
    <Section id="how" size="sm" className="max-w-4xl">
      <SectionHeading
        eyebrow={t('how.eyebrow')}
        title={t('how.title')}
        description={t('how.description')}
      />

      <div className="stagger mt-12 grid gap-6 sm:grid-cols-3">
        {STEPS.map((step) => (
          <div key={step.titleKey} className="card-flat relative p-6 text-center">
            {/* Step number */}
            <span className="absolute end-4 top-4 flex h-7 w-7 items-center justify-center rounded-full bg-[var(--brand-soft)] text-xs font-bold text-[var(--brand)]">
              {step.num}
            </span>
            <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-[var(--brand-soft)] text-[var(--brand)]">
              <Icon name={step.icon} size={22} />
            </div>
            <h3 className="text-base font-semibold text-[var(--text-primary)]">{t(step.titleKey)}</h3>
            <p className="mt-1.5 text-sm leading-relaxed text-[var(--text-secondary)]">{t(step.descKey)}</p>
          </div>
        ))}
      </div>
    </Section>
  );
}
