import rss from '@astrojs/rss';
import { getFeed, getTextos } from './collections';
import { formatDate, sectionPath, type Lang } from './i18n';
import { t } from './ui-strings';

const POST_TITLE_LENGTH = 80;

export async function buildRss(lang: Lang, site: URL | undefined): Promise<Response> {
  const [textos, feed] = await Promise.all([getTextos(lang), getFeed(lang)]);
  const items = [
    ...textos.map((texto) => ({
      title: texto.entry.data.titulo,
      description: texto.entry.data.resumo,
      pubDate: texto.entry.data.data,
      link: sectionPath(lang, 'texts', texto.slug),
      categories: texto.entry.data.tags,
    })),
    ...feed.map((post) => {
      const text = (post.entry.body ?? '').replace(/\s+/g, ' ').trim();
      return {
        title: text.slice(0, POST_TITLE_LENGTH) || `${t(lang, 'feedPostTitle')} ${formatDate(post.entry.data.data, lang)}`,
        description: text,
        pubDate: post.entry.data.data,
        link: sectionPath(lang, 'feed', post.slug),
        categories: post.entry.data.tags,
      };
    }),
  ].toSorted((a, b) => b.pubDate.getTime() - a.pubDate.getTime());

  return rss({
    title: t(lang, 'rssTitle'),
    description: t(lang, 'rssDescription'),
    site: site ?? 'https://joaogbarros.github.io',
    items,
    customData: `<language>${lang === 'pt' ? 'pt-br' : 'en'}</language>`,
  });
}
