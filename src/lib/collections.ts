import { getCollection, type CollectionEntry } from 'astro:content';
import { isPublished, pinnedFirst, publishedProjectSlugs, validateProjectRefs } from './content';
import { localizeAll, otherLang, parseEntryId, type Lang, type Localized } from './i18n';

export type Projeto = CollectionEntry<'projetos'>;
export type Texto = CollectionEntry<'textos'>;
export type Post = CollectionEntry<'feed'>;
export type CvData = CollectionEntry<'cv'>['data'];

type Localizable = 'projetos' | 'textos' | 'feed';

async function published<C extends Localizable>(collection: C): Promise<CollectionEntry<C>[]> {
  const entries = (await getCollection(collection)) as CollectionEntry<C>[];
  return entries.filter((entry) => isPublished(entry));
}

let validation: Promise<void> | undefined;

/** Fails the build when a text or post points to a project that does not exist. */
function ensureValidRefs(): Promise<void> {
  validation ??= (async () => {
    const [projetos, textos, feed] = await Promise.all([
      getCollection('projetos'),
      getCollection('textos'),
      getCollection('feed'),
    ]);
    const projectSlugs = publishedProjectSlugs(projetos);
    const refs = [...textos, ...feed]
      .filter((entry) => isPublished(entry))
      .map((entry) => ({ source: `${entry.collection}/${entry.id}`, projeto: entry.data.projeto }));
    validateProjectRefs(refs, projectSlugs);
  })();
  return validation;
}

const byDateDesc = (a: { entry: { data: { data: Date } } }, b: { entry: { data: { data: Date } } }) =>
  b.entry.data.data.getTime() - a.entry.data.data.getTime();

export async function getProjects(lang: Lang): Promise<Localized<Projeto>[]> {
  const items = localizeAll(await published('projetos'), lang);
  return items.toSorted((a, b) => {
    const da = a.entry.data.destaque ?? Number.POSITIVE_INFINITY;
    const db = b.entry.data.destaque ?? Number.POSITIVE_INFINITY;
    return da !== db ? da - db : a.entry.data.titulo.localeCompare(b.entry.data.titulo);
  });
}

export async function getTextos(lang: Lang): Promise<Localized<Texto>[]> {
  await ensureValidRefs();
  return pinnedFirst(localizeAll(await published('textos'), lang).toSorted(byDateDesc));
}

export async function getFeed(lang: Lang): Promise<Localized<Post>[]> {
  await ensureValidRefs();
  return localizeAll(await published('feed'), lang).toSorted(byDateDesc);
}

export async function getCv(lang: Lang): Promise<CvData> {
  const entries = await getCollection('cv');
  const pick = (l: Lang) => entries.find((entry) => entry.id === l);
  const entry = pick(lang) ?? pick(otherLang(lang));
  if (!entry) throw new Error('Nenhum currículo encontrado em src/data/cv/.');
  return entry.data;
}

/** Published slugs in any language: both language routes are generated for each. */
export async function getAllSlugs(collection: Localizable): Promise<string[]> {
  const entries = await published(collection);
  return [...new Set(entries.map((entry) => parseEntryId(entry.id).slug))];
}
