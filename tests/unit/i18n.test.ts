import { describe, expect, test } from 'vitest';
import {
  chooseLang,
  formatDate,
  localizeAll,
  parseEntryId,
  sectionPath,
  switchLangPath,
} from '../../src/lib/i18n';
import { t, UI } from '../../src/lib/ui-strings';

describe('sectionPath', () => {
  test('builds prefixed paths with translated section slugs', () => {
    expect(sectionPath('pt', 'home')).toBe('/pt/');
    expect(sectionPath('pt', 'projects', 'here-to-slay')).toBe('/pt/projetos/here-to-slay/');
    expect(sectionPath('en', 'texts')).toBe('/en/writing/');
    expect(sectionPath('en', 'feed')).toBe('/en/updates/');
    expect(sectionPath('pt', 'cv')).toBe('/pt/curriculo/');
  });
});

describe('switchLangPath', () => {
  test('maps the section segment and keeps the rest', () => {
    expect(switchLangPath('/pt/projetos/here-to-slay/', 'en')).toBe('/en/projects/here-to-slay/');
    expect(switchLangPath('/en/updates/2026-10-01-v13/', 'pt')).toBe('/pt/atualizacoes/2026-10-01-v13/');
    expect(switchLangPath('/pt/textos/projeto/calmo/', 'en')).toBe('/en/writing/projeto/calmo/');
    expect(switchLangPath('/en/', 'pt')).toBe('/pt/');
  });

  test('falls back to the home page for unknown paths', () => {
    expect(switchLangPath('/qualquer-coisa', 'pt')).toBe('/pt/');
    expect(switchLangPath('/pt/nao-existe/x/', 'en')).toBe('/en/');
  });
});

describe('parseEntryId', () => {
  test('splits slug and language', () => {
    expect(parseEntryId('here-to-slay/pt')).toEqual({ slug: 'here-to-slay', lang: 'pt' });
  });

  test('rejects unknown languages naming the id', () => {
    expect(() => parseEntryId('here-to-slay/es')).toThrow(/here-to-slay\/es/);
    expect(() => parseEntryId('solto')).toThrow(/solto/);
  });
});

describe('localizeAll', () => {
  test('returns one item per slug, preferring the requested language', () => {
    const entries = [{ id: 'a/pt' }, { id: 'a/en' }, { id: 'b/pt' }];
    const result = localizeAll(entries, 'en').map((l) => [l.slug, l.lang, l.isFallback]);
    expect(result).toEqual([
      ['a', 'en', false],
      ['b', 'pt', true],
    ]);
  });

  test('does not mutate the input', () => {
    const entries = Object.freeze([{ id: 'b/en' }, { id: 'a/en' }]);
    expect(() => localizeAll(entries, 'pt')).not.toThrow();
  });
});

describe('chooseLang', () => {
  test('uses the browser language when nothing is stored', () => {
    expect(chooseLang(null, ['pt-BR', 'en'])).toBe('pt');
    expect(chooseLang(null, ['pt-PT'])).toBe('pt');
    expect(chooseLang(null, ['es-ES'])).toBe('en');
    expect(chooseLang(null, [])).toBe('en');
  });

  test('prefers a valid stored choice and ignores an invalid one', () => {
    expect(chooseLang('pt', ['en-US'])).toBe('pt');
    expect(chooseLang('klingon', ['pt-PT'])).toBe('pt');
  });
});

describe('formatDate', () => {
  test('formats in UTC so the day never shifts', () => {
    const date = new Date('2026-10-01');
    expect(formatDate(date, 'pt')).toMatch(/^1 de out\.? de 2026$/);
    expect(formatDate(date, 'en')).toBe('Oct 1, 2026');
  });
});

describe('ui strings', () => {
  test('both languages define exactly the same keys', () => {
    expect(Object.keys(UI.pt).sort()).toEqual(Object.keys(UI.en).sort());
  });

  test('t returns the string for the language', () => {
    expect(t('pt', 'navProjects')).toBe('Projetos');
    expect(t('en', 'navProjects')).toBe('Projects');
  });
});
