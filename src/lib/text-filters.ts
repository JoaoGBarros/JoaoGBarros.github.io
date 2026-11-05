import { getTextos } from './collections';
import { collectTags } from './content';
import { LANGS } from './i18n';

/** Filter pages are generated for the union of both languages, so both routes always exist. */
export async function getTextFilterPaths(): Promise<{ projects: string[]; tags: string[] }> {
  const all = (await Promise.all(LANGS.map((lang) => getTextos(lang)))).flat();
  const projects = [...new Set(all.flatMap((t) => (t.entry.data.projeto ? [t.entry.data.projeto] : [])))];
  return { projects: projects.toSorted(), tags: collectTags(all) };
}
