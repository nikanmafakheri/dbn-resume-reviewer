import { useLanguage } from '../../context/LanguageContext';
import { Icon } from '../ui/Icon';

const SOCIALS = [
  { name: 'instagram', href: 'https://instagram.com/devbynikan', label: '@devbynikan' },
  { name: 'linkedin', href: 'https://linkedin.com/in/nikanmafakheri', label: 'nikanmafakheri' },
  { name: 'github', href: 'https://github.com/nikanmafakheri', label: 'nikanmafakheri' },
] as const;

export function Footer() {
  const { t } = useLanguage();

  return (
    <footer className="border-t border-[var(--border)] bg-[var(--surface)]">
      <div className="container-dbn flex flex-col gap-8 py-12 sm:flex-row sm:items-center sm:justify-between">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <img
            src="/logo.jpg"
            alt="DevByNikan"
            className="h-9 w-9 rounded-full object-cover ring-2 ring-[var(--border)]"
          />
          <div>
            <p className="text-sm font-semibold tracking-tight text-[var(--text-primary)]">DevByNikan</p>
            <p className="mt-0.5 text-xs text-[var(--text-muted)]">{t('footer.tagline')}</p>
          </div>
        </div>

        {/* Socials */}
        <div className="flex flex-wrap items-center gap-2">
          {SOCIALS.map((s) => (
            <a
              key={s.name}
              href={s.href}
              target="_blank"
              rel="noopener noreferrer"
              className="group inline-flex items-center gap-2 rounded-full border border-transparent px-3 py-1.5 text-sm font-medium text-[var(--text-muted)] transition-colors duration-200 hover:border-[var(--border)] hover:bg-[var(--surface-soft)] hover:text-[var(--text-primary)]"
              aria-label={`${s.label} (opens in a new tab)`}
            >
              <Icon name={s.name} size={16} className="transition-transform duration-200 group-hover:scale-110" />
              <span>{s.label}</span>
            </a>
          ))}
        </div>
      </div>

      <div className="border-t border-[var(--border)] py-5">
        <p className="px-4 text-center text-xs text-[var(--text-muted)]">
          &copy; {new Date().getFullYear()} DevByNikan. {t('footer.copyright')}
        </p>
      </div>
    </footer>
  );
}
