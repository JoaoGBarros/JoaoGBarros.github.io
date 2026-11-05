export type Lang = 'pt' | 'en';

export const LANGS: readonly Lang[] = ['pt', 'en'];
export const DEFAULT_LANG: Lang = 'en';

export type Section = 'home' | 'projects' | 'texts' | 'feed' | 'downloads' | 'cv';
type ContentSection = Exclude<Section, 'home'>;

const SECTION_SLUGS: Record<Lang, Record<ContentSection, string>> = {
  pt: {
    projects: 'projetos',
    texts: 'textos',
    feed: 'atualizacoes',
    downloads: 'downloads',
    cv: 'curriculo',
  },
  en: {
    projects: 'projects',
    texts: 'writing',
    feed: 'updates',
    downloads: 'downloads',
    cv: 'cv',
  },
};

export function isLang(value: unknown): value is Lang {
  return typeof value === 'string' && (LANGS as readonly string[]).includes(value);
}

/** BCP 47 tag for `lang` attributes. */
export function htmlLang(lang: Lang): string {
  return lang === 'pt' ? 'pt-BR' : 'en';
}

/** `lang` attribute for content written in `contentLang` inside a page in `lang`; omitted when equal. */
export function contentLangAttr(lang: Lang, contentLang: Lang): string | undefined {
  return contentLang === lang ? undefined : htmlLang(contentLang);
}

export function otherLang(lang: Lang): Lang {
  return lang === 'pt' ? 'en' : 'pt';
}

export function sectionPath(lang: Lang, section: Section, slug?: string): string {
  if (section === 'home') return `/${lang}/`;
  const base = `/${lang}/${SECTION_SLUGS[lang][section]}/`;
  return slug ? `${base}${slug}/` : base;
}

function sectionFromSlug(lang: Lang, segment: string): ContentSection | undefined {
  const entries = Object.entries(SECTION_SLUGS[lang]) as [ContentSection, string][];
  return entries.find(([, value]) => value === segment)?.[0];
}

/** Same page in the other language; unknown paths go to the target home page. */
export function switchLangPath(path: string, target: Lang): string {
  const [first, second, ...rest] = path.split('/').filter(Boolean);
  if (!isLang(first)) return sectionPath(target, 'home');
  if (second === undefined) return sectionPath(target, 'home');
  const section = sectionFromSlug(first, second);
  if (!section) return sectionPath(target, 'home');
  const tail = rest.length > 0 ? `${rest.join('/')}/` : '';
  return `${sectionPath(target, section)}${tail}`;
}

export function parseEntryId(id: string): { slug: string; lang: Lang } {
  const cut = id.lastIndexOf('/');
  const slug = cut > 0 ? id.slice(0, cut) : '';
  const lang = id.slice(cut + 1);
  if (!slug || !isLang(lang)) {
    throw new Error(`Conteúdo com id inválido "${id}": esperado "<slug>/pt" ou "<slug>/en".`);
  }
  return { slug, lang };
}

export interface Localized<E> {
  slug: string;
  entry: E;
  /** Language the content is actually written in. */
  lang: Lang;
  isFallback: boolean;
}

/** One item per slug: the requested language, or the other one as a fallback. */
export function localizeAll<E extends { id: string }>(
  entries: readonly E[],
  lang: Lang,
): Localized<E>[] {
  const bySlug = new Map<string, Partial<Record<Lang, E>>>();
  for (const entry of entries) {
    const { slug, lang: entryLang } = parseEntryId(entry.id);
    bySlug.set(slug, { ...bySlug.get(slug), [entryLang]: entry });
  }
  return [...bySlug.entries()].map(([slug, versions]) => {
    const own = versions[lang];
    if (own) return { slug, entry: own, lang, isFallback: false };
    const fallbackLang = otherLang(lang);
    return { slug, entry: versions[fallbackLang] as E, lang: fallbackLang, isFallback: true };
  });
}

export function chooseLang(stored: string | null, navigatorLangs: readonly string[]): Lang {
  if (isLang(stored)) return stored;
  const first = navigatorLangs[0]?.toLowerCase() ?? '';
  return first.startsWith('pt') ? 'pt' : DEFAULT_LANG;
}

const DATE_LOCALES: Record<Lang, string> = { pt: 'pt-BR', en: 'en-US' };

export function formatDate(date: Date, lang: Lang): string {
  return new Intl.DateTimeFormat(DATE_LOCALES[lang], {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    timeZone: 'UTC',
  }).format(date);
}
