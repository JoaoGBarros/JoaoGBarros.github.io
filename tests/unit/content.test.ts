import { describe, expect, test } from 'vitest';
import type { Localized } from '../../src/lib/i18n';
import {
  collectTags,
  downloadsByProject,
  featured,
  isPublished,
  isValidTag,
  pinnedFirst,
  publishedProjectSlugs,
  seriesFor,
  seriesNeighbors,
  validateProjectRefs,
} from '../../src/lib/content';

function loc<D>(slug: string, data: D): Localized<{ id: string; data: D }> {
  return { slug, entry: { id: `${slug}/pt`, data }, lang: 'pt', isFallback: false };
}

const slugs = (items: { slug: string }[]) => items.map((i) => i.slug);

describe('isPublished', () => {
  test('drafts are hidden, everything else is published', () => {
    expect(isPublished({ data: { rascunho: true } })).toBe(false);
    expect(isPublished({ data: { rascunho: false } })).toBe(true);
    expect(isPublished({ data: {} })).toBe(true);
  });
});

describe('featured', () => {
  test('keeps only projects with destaque, ordered ascending', () => {
    const projects = [loc('c', { destaque: 2 }), loc('a', {}), loc('b', { destaque: 1 })];
    expect(slugs(featured(projects))).toEqual(['b', 'c']);
  });
});

describe('seriesFor and seriesNeighbors', () => {
  const textos = [
    loc('t1', { projeto: 'hts', ordem: 2, data: new Date('2026-03-01') }),
    loc('t2', { projeto: 'hts', ordem: 1, data: new Date('2026-04-01') }),
    loc('t3', { projeto: 'hts', data: new Date('2026-01-01') }),
    loc('t5', { projeto: 'hts', data: new Date('2026-02-01') }),
    loc('t4', { projeto: 'outro', ordem: 1, data: new Date('2026-01-01') }),
    loc('t6', { data: new Date('2026-01-01') }),
  ];

  test('filters by project, orders by ordem then date, unordered last', () => {
    expect(slugs(seriesFor(textos, 'hts'))).toEqual(['t2', 't1', 't3', 't5']);
  });

  test('neighbors inside the series', () => {
    const series = seriesFor(textos, 'hts');
    const middle = seriesNeighbors(series, 't1');
    expect(middle.prev?.slug).toBe('t2');
    expect(middle.next?.slug).toBe('t3');
    const first = seriesNeighbors(series, 't2');
    expect(first.prev).toBeUndefined();
    expect(first.next?.slug).toBe('t1');
    expect(seriesNeighbors(series, 'nao-existe')).toEqual({});
  });
});

describe('downloadsByProject', () => {
  test('omits projects without downloads and keeps input order', () => {
    const file = {
      rotulo: 'APK',
      plataforma: 'Android',
      versao: '1.0',
      tamanho: '12 MB',
      data: new Date('2026-01-01'),
      url: 'https://example.com/a.apk',
    };
    const projects = [loc('x', { downloads: [file] }), loc('y', { downloads: [] }), loc('z', { downloads: [file, file] })];
    const result = downloadsByProject(projects);
    expect(result.map((r) => [r.project.slug, r.downloads.length])).toEqual([
      ['x', 1],
      ['z', 2],
    ]);
  });
});

describe('collectTags', () => {
  test('unique and sorted', () => {
    const items = [loc('a', { tags: ['tecnico', 'kafka'] }), loc('b', { tags: ['tecnico'] }), loc('c', { tags: [] })];
    expect(collectTags(items)).toEqual(['kafka', 'tecnico']);
  });
});

describe('validateProjectRefs', () => {
  test('lists every invalid reference', () => {
    expect(() =>
      validateProjectRefs(
        [
          { source: 'textos/x/pt', projeto: 'here-to-sly' },
          { source: 'feed/y/en', projeto: 'nope' },
          { source: 'textos/z/pt' },
        ],
        new Set(['here-to-slay']),
      ),
    ).toThrow(/textos\/x\/pt → projeto 'here-to-sly' não existe[\s\S]*feed\/y\/en → projeto 'nope'/);
  });

  test('accepts valid and missing references', () => {
    expect(() =>
      validateProjectRefs([{ source: 's', projeto: 'here-to-slay' }, { source: 't' }], new Set(['here-to-slay'])),
    ).not.toThrow();
  });
});

describe('publishedProjectSlugs', () => {
  test('draft projects are not valid reference targets', () => {
    const entries = [
      { id: 'here-to-slay/pt', data: { rascunho: false } },
      { id: 'here-to-slay/en', data: {} },
      { id: 'secreto/pt', data: { rascunho: true } },
    ];
    expect([...publishedProjectSlugs(entries)]).toEqual(['here-to-slay']);
    expect(() =>
      validateProjectRefs([{ source: 'textos/a/pt', projeto: 'secreto' }], publishedProjectSlugs(entries)),
    ).toThrow(/projeto 'secreto' não existe/);
  });
});

describe('isValidTag', () => {
  test('accepts words, accents, spaces, digits and safe punctuation', () => {
    for (const tag of ['tecnico', 'experiência', 'dev ops', 'kafka', 'c++', 'node.js', 'web_2']) {
      expect(isValidTag(tag), tag).toBe(true);
    }
  });

  test('rejects characters that break URLs', () => {
    for (const tag of ['C#', 'a?b', 'a/b', '100%', '']) {
      expect(isValidTag(tag), tag).toBe(false);
    }
  });
});

describe('pinnedFirst', () => {
  test('moves pinned items to the top and keeps the rest in order', () => {
    const items = [
      loc('novo', { fixado: false }),
      loc('meio', {}),
      loc('sobre-mim', { fixado: true }),
      loc('velho', {}),
    ];
    expect(slugs(pinnedFirst(items))).toEqual(['sobre-mim', 'novo', 'meio', 'velho']);
  });

  test('does not mutate the input', () => {
    const items = Object.freeze([loc('a', {}), loc('b', { fixado: true })]);
    expect(slugs(pinnedFirst(items))).toEqual(['b', 'a']);
  });
});
