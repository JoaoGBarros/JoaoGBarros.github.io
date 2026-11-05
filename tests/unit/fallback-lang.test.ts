import { experimental_AstroContainer as AstroContainer } from 'astro/container';
import { expect, test } from 'vitest';
import FallbackNotice from '../../src/components/FallbackNotice.astro';
import BaseLayout from '../../src/layouts/BaseLayout.astro';

test('the fallback notice is marked with the interface language', async () => {
  const container = await AstroContainer.create();
  const html = await container.renderToString(FallbackNotice, { props: { lang: 'pt', contentLang: 'en' } });
  expect(html).toMatch(/<p[^>]*class="fallback"[^>]*lang="pt-BR"|<p[^>]*lang="pt-BR"[^>]*class="fallback"/);
});

test('main keeps the interface language on fallback pages', async () => {
  const container = await AstroContainer.create();
  const html = await container.renderToString(BaseLayout, {
    props: { lang: 'pt', title: 'x', description: 'x', path: '/pt/textos/x/', contentLang: 'en' },
  });
  expect(html).toMatch(/<html lang="pt-BR"/);
  expect(html).not.toMatch(/<main[^>]*\blang=/);
});
