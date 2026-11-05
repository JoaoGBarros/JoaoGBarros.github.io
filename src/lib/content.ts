import { parseEntryId, type Localized } from './i18n';

/** Pure content rules. Entries only need `{ data }`, so tests use plain objects. */

export interface Download {
  rotulo: string;
  plataforma: string;
  versao: string;
  tamanho: string;
  data: Date;
  url: string;
}

type WithData<D> = { data: D };

export function isPublished(entry: WithData<{ rascunho?: boolean }>): boolean {
  return entry.data.rascunho !== true;
}

export function featured<E extends WithData<{ destaque?: number }>>(
  projects: readonly Localized<E>[],
): Localized<E>[] {
  return projects
    .filter((p) => p.entry.data.destaque !== undefined)
    .toSorted((a, b) => (a.entry.data.destaque ?? 0) - (b.entry.data.destaque ?? 0));
}

type SeriesData = { projeto?: string; ordem?: number; data: Date };

function compareSeries(a: SeriesData, b: SeriesData): number {
  const orderA = a.ordem ?? Number.POSITIVE_INFINITY;
  const orderB = b.ordem ?? Number.POSITIVE_INFINITY;
  if (orderA !== orderB) return orderA - orderB;
  return a.data.getTime() - b.data.getTime();
}

export function seriesFor<E extends WithData<SeriesData>>(
  textos: readonly Localized<E>[],
  projectSlug: string,
): Localized<E>[] {
  return textos
    .filter((t) => t.entry.data.projeto === projectSlug)
    .toSorted((a, b) => compareSeries(a.entry.data, b.entry.data));
}

export function seriesNeighbors<T extends { slug: string }>(
  series: readonly T[],
  slug: string,
): { prev?: T; next?: T } {
  const index = series.findIndex((item) => item.slug === slug);
  if (index === -1) return {};
  const prev = series[index - 1];
  const next = series[index + 1];
  return { ...(prev && { prev }), ...(next && { next }) };
}

export function downloadsByProject<E extends WithData<{ downloads?: Download[] }>>(
  projects: readonly Localized<E>[],
): { project: Localized<E>; downloads: Download[] }[] {
  return projects
    .map((project) => ({ project, downloads: project.entry.data.downloads ?? [] }))
    .filter((group) => group.downloads.length > 0);
}

export function collectTags(items: readonly { entry: WithData<{ tags?: string[] }> }[]): string[] {
  const all = items.flatMap((item) => item.entry.data.tags ?? []);
  return [...new Set(all)].toSorted((a, b) => a.localeCompare(b));
}

/** Pinned items (`fixado: true`) come first; everything else keeps its current order. */
export function pinnedFirst<T extends { entry: WithData<{ fixado?: boolean }> }>(items: readonly T[]): T[] {
  const isPinned = (item: T) => item.entry.data.fixado === true;
  return [...items.filter(isPinned), ...items.filter((item) => !isPinned(item))];
}

/** Slugs of published projects only: a draft project is not a valid reference target. */
export function publishedProjectSlugs(
  entries: readonly { id: string; data: { rascunho?: boolean } }[],
): Set<string> {
  return new Set(entries.filter((entry) => isPublished(entry)).map((entry) => parseEntryId(entry.id).slug));
}

/** Tags become URL segments, so `#`, `?`, `/` and `%` are not allowed. */
const TAG_PATTERN = /^[\p{L}\p{N}][\p{L}\p{N} _.+-]*$/u;

export function isValidTag(tag: string): boolean {
  return TAG_PATTERN.test(tag);
}

export function validateProjectRefs(
  refs: readonly { source: string; projeto?: string }[],
  projectSlugs: ReadonlySet<string>,
): void {
  const problems = refs
    .filter((ref) => ref.projeto !== undefined && !projectSlugs.has(ref.projeto))
    .map((ref) => `${ref.source} → projeto '${ref.projeto}' não existe`);
  if (problems.length > 0) {
    throw new Error(`Referências de projeto inválidas:\n${problems.join('\n')}`);
  }
}
