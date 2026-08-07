import { createContext, useContext, useState, useCallback, type ReactNode } from 'react';
import en from '../i18n/en.json';
import fa from '../i18n/fa.json';
import type { TranslationKey } from '../types/i18n';

type Locale = 'en' | 'fa';
type TranslationValue = string | Record<string, unknown>;

interface LanguageContextValue {
  locale: Locale;
  t: (key: TranslationKey) => string;
  toggleLanguage: () => void;
  dir: 'ltr' | 'rtl';
}

const LanguageContext = createContext<LanguageContextValue | null>(null);

const translations: Record<Locale, Record<string, TranslationValue>> = { en, fa };

function getNestedValue(obj: Record<string, TranslationValue>, path: string): string {
  const keys = path.split('.');
  let current: TranslationValue = obj;
  for (const key of keys) {
    if (typeof current === 'object' && current !== null && key in current) {
      current = (current as Record<string, TranslationValue>)[key];
    } else {
      return path;
    }
  }
  return typeof current === 'string' ? current : path;
}

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [locale, setLocale] = useState<Locale>(() => {
    const saved = localStorage.getItem('locale');
    return (saved === 'en' || saved === 'fa') ? saved : 'en';
  });

  const t = useCallback((key: TranslationKey): string => {
    const value = getNestedValue(translations[locale] as Record<string, TranslationValue>, key);
    // Fall back to the English entry (the source of truth) when the active
    // locale is missing a key, and surface the gap in dev so it gets fixed.
    if (value === key && locale !== 'en') {
      const enValue = getNestedValue(en, key);
      if (enValue !== key) {
        if (import.meta.env.DEV) console.warn(`[i18n] Missing key "${key}" in "${locale}"`);
        return enValue;
      }
    }
    return value;
  }, [locale]);

  const toggleLanguage = useCallback(() => {
    setLocale(prev => {
      const next = prev === 'en' ? 'fa' : 'en';
      localStorage.setItem('locale', next);
      document.documentElement.dir = next === 'fa' ? 'rtl' : 'ltr';
      document.documentElement.lang = next;
      return next;
    });
  }, []);

  const dir = locale === 'fa' ? 'rtl' : 'ltr';

  return (
    <LanguageContext.Provider value={{ locale, t, toggleLanguage, dir }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error('useLanguage must be used within LanguageProvider');
  return ctx;
}
