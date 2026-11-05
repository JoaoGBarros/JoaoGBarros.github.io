// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Para usar um domínio próprio: troque `site` e adicione public/CNAME.
export default defineConfig({
  site: 'https://joaogbarros.github.io',
  trailingSlash: 'always',
  integrations: [sitemap({ filter: (page) => !page.endsWith('/404/') })],
});
