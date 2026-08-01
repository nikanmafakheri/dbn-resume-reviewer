/**
 * Regenerate `src/types/i18n.ts` from `src/i18n/en.json`.
 *
 * Usage: node scripts/gen-i18n-types.mjs
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, '..', 'src');

const en = JSON.parse(readFileSync(join(src, 'i18n', 'en.json'), 'utf8'));

function collect(o, p = '') {
  let out = [];
  for (const k of Object.keys(o)) {
    const path = p ? `${p}.${k}` : k;
    if (typeof o[k] === 'object' && o[k] !== null) {
      out.push(...collect(o[k], path));
    } else {
      out.push(path);
    }
  }
  return out;
}

const keys = collect(en).sort();
const body = keys.map((k) => `  '${k}'`).join(' |\n');

const content = `/**
 * Generated from src/i18n/en.json — do not edit by hand.
 * Regenerate with: node scripts/gen-i18n-types.mjs
 */
export type TranslationKey =
${body};
`;

writeFileSync(join(src, 'types', 'i18n.ts'), content);
console.log(`Wrote ${keys.length} translation keys to src/types/i18n.ts`);
