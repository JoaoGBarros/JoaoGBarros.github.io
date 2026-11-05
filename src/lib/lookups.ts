import type { Projeto, Texto } from './collections';
import type { Localized } from './i18n';

export function projectTitleMap(projects: readonly Localized<Projeto>[]): Map<string, string> {
  return new Map(projects.map((p) => [p.slug, p.entry.data.titulo]));
}

export function textCountMap(textos: readonly Localized<Texto>[]): Map<string, number> {
  return textos.reduce((counts, texto) => {
    const projeto = texto.entry.data.projeto;
    return projeto ? new Map(counts).set(projeto, (counts.get(projeto) ?? 0) + 1) : counts;
  }, new Map<string, number>());
}
