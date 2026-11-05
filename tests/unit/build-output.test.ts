import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { describe, expect, test } from 'vitest';

const DIST = join(process.cwd(), 'dist');
const hasDist = existsSync(DIST);

function walk(dir: string): string[] {
  return readdirSync(dir, { withFileTypes: true }).flatMap((d) =>
    d.isDirectory() ? walk(join(dir, d.name)) : [join(dir, d.name)],
  );
}

const textFiles = (): string[] => walk(DIST).filter((f) => /\.(html|xml|txt|json)$/.test(f));
const rel = (f: string) => relative(DIST, f).split(sep).join('/');

function grepDist(pattern: RegExp): string[] {
  return textFiles()
    .filter((f) => pattern.test(readFileSync(f, 'utf8')))
    .map(rel);
}

const SECTION_PAIRS: [string, string][] = [
  ['pt/projetos/', 'en/projects/'],
  ['pt/textos/', 'en/writing/'],
  ['pt/atualizacoes/', 'en/updates/'],
  ['pt/downloads/', 'en/downloads/'],
  ['pt/curriculo/', 'en/cv/'],
];

function missingCounterparts(): string[] {
  const pages = new Set(walk(DIST).map(rel).filter((p) => p.endsWith('index.html')));
  const counterpart = (page: string): string | undefined => {
    for (const [pt, en] of SECTION_PAIRS) {
      if (page.startsWith(pt)) return en + page.slice(pt.length);
      if (page.startsWith(en)) return pt + page.slice(en.length);
    }
    if (page === 'pt/index.html') return 'en/index.html';
    if (page === 'en/index.html') return 'pt/index.html';
    return undefined;
  };
  return [...pages].flatMap((page) => {
    const other = counterpart(page);
    return other && !pages.has(other) ? [`${page} → ${other}`] : [];
  });
}

describe.skipIf(!hasDist)('build output (run `npm run build` first)', () => {
  test('the phone number never reaches HTML, XML or JSON', () => {
    // Any Brazilian mobile number, e.g. "+55 27 9xxxx-xxxx" or "(27) 9xxxx-xxxx".
    expect(grepDist(/(\+55\s*)?\(\d{2}\)\s*9\d{4}[-\s]?\d{4}|\+55\s*\d{2}\s*9\d{4}[-\s]?\d{4}/)).toEqual([]);
  });

  test('draft templates are never published', () => {
    expect(grepDist(/exemplo-serie|2026-11-04-exemplo/)).toEqual([]);
  });

  test('every page exists in both languages', () => {
    expect(missingCounterparts()).toEqual([]);
  });

  test('sitemap lists both languages and not the 404 page', () => {
    const sitemap = readFileSync(join(DIST, 'sitemap-0.xml'), 'utf8');
    expect(sitemap).not.toMatch(/404/);
    expect(sitemap).toMatch(/\/pt\/projetos\/here-to-slay\//);
    expect(sitemap).toMatch(/\/en\/projects\/here-to-slay\//);
  });

  test('both RSS feeds exist and declare their language', () => {
    expect(readFileSync(join(DIST, 'pt/rss.xml'), 'utf8')).toMatch(/<language>pt-br<\/language>/);
    expect(readFileSync(join(DIST, 'en/rss.xml'), 'utf8')).toMatch(/<language>en<\/language>/);
  });

  test('CV PDFs are published for both languages', () => {
    expect(existsSync(join(DIST, 'cv/cv-pt.pdf'))).toBe(true);
    expect(existsSync(join(DIST, 'cv/cv-en.pdf'))).toBe(true);
  });
});
