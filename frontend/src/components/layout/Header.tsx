import { useLanguage } from '../../context/LanguageContext';
import { useTheme } from '../../context/ThemeContext';
import { Icon } from '../ui/Icon';

export function Header() {
  const { t, locale, toggleLanguage } = useLanguage();
  const { isDark, toggleTheme } = useTheme();

  return (
    <header className="sticky top-0 z-50 border-b border-[var(--nav-border)] bg-[var(--nav-bg)] backdrop-blur-md supports-[backdrop-filter]:bg-[var(--nav-bg)]">
      <div className="container-dbn flex h-16 items-center gap-3">
        {/* Logo */}
        <a href="#top" className="group flex min-w-0 items-center gap-2.5" aria-label="DevByNikan — Home">
          <img
            src="/logo.jpg"
            alt="DevByNikan"
            className="h-9 w-9 shrink-0 rounded-full object-cover ring-2 ring-[var(--border)] transition-transform duration-200 group-hover:scale-105"
          />
          <span className="truncate text-[15px] font-bold tracking-tight text-[var(--text-primary)] transition-colors">
            {t('nav.title')}
          </span>
        </a>

        <div className="flex-1" />

        {/* Theme toggle */}
        <button
          type="button"
          onClick={toggleTheme}
          aria-pressed={isDark}
          aria-label={isDark ? t('theme.light') : t('theme.dark')}
          title={isDark ? t('theme.light') : t('theme.dark')}
          className="flex h-9 w-9 items-center justify-center rounded-full border border-[var(--border)] bg-[var(--surface)] text-[var(--text-secondary)] transition-all duration-200 hover:border-[var(--border-strong)] hover:text-[var(--text-primary)] hover:shadow-sm"
        >
          <Icon
            name={isDark ? 'sun' : 'moon'}
            size={17}
            className="transition-transform duration-300"
          />
        </button>

        {/* Language toggle */}
        <button
          type="button"
          onClick={toggleLanguage}
          aria-pressed={locale === 'fa'}
          aria-label={t('nav.switchLang')}
          title={t('nav.switchLang')}
          className="flex h-9 items-center gap-1.5 rounded-full border border-[var(--border)] bg-[var(--surface)] px-3 text-sm font-semibold text-[var(--text-secondary)] transition-all duration-200 hover:border-[var(--border-strong)] hover:text-[var(--text-primary)] hover:shadow-sm"
        >
          <Icon name="globe" size={16} />
          <span className="uppercase">{locale === 'en' ? 'FA' : 'EN'}</span>
        </button>
      </div>
    </header>
  );
}
