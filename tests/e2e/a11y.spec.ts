import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

const PAGES = [
  '/pt/',
  '/en/',
  '/pt/projetos/',
  '/pt/projetos/here-to-slay/',
  '/en/projects/centro-academico/',
  '/pt/projetos/hockey-de-mesa/',
  '/en/projects/levitador-magnetico/',
  '/pt/textos/um-pouco-sobre-mim/',
  '/pt/textos/',
  '/en/updates/',
  '/pt/downloads/',
  '/pt/curriculo/',
  '/en/cv/',
];

for (const path of PAGES) {
  test(`no WCAG A/AA violations on ${path}`, async ({ page }) => {
    await page.goto(path);
    const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
    const summary = results.violations.map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(' ')).join(', ')}`);
    expect(summary).toEqual([]);
  });
}
