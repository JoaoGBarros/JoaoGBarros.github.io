import { expect, test } from '@playwright/test';

const EMAIL = 'mailto:jgabriel.b.rocha@gmail.com';
/** Any Brazilian phone number, e.g. "+55 27 9xxxx-xxxx" or "(27) 9xxxx-xxxx". */
const BR_PHONE = /(\+55\s*)?\(?\d{2}\)?\s*9\d{4}[-\s]?\d{4}/;

for (const lang of ['pt', 'en'] as const) {
  test(`home page renders in ${lang}`, async ({ page }) => {
    await page.goto(`/${lang}/`);
    await expect(page.getByRole('heading', { level: 1 })).toContainText('João Gabriel');
    await expect(page.locator(`main a[href="${EMAIL}"]`).first()).toBeVisible();
    await expect(page.getByRole('link', { name: 'Here To Slay' }).first()).toBeVisible();
  });
}

test('language switch keeps the same page', async ({ page }) => {
  await page.goto('/pt/projetos/here-to-slay/');
  await page.locator('a.lang-switch').click();
  await expect(page).toHaveURL(/\/en\/projects\/here-to-slay\/$/);
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Here To Slay');
});

test.describe('root redirect follows the browser language', () => {
  test.describe('pt-BR', () => {
    test.use({ locale: 'pt-BR' });
    test('goes to /pt/', async ({ page }) => {
      await page.goto('/');
      await expect(page).toHaveURL(/\/pt\/$/);
    });
  });

  test.describe('es-ES', () => {
    test.use({ locale: 'es-ES' });
    test('goes to /en/', async ({ page }) => {
      await page.goto('/');
      await expect(page).toHaveURL(/\/en\/$/);
    });
  });

  test.describe('saved choice', () => {
    test.use({ locale: 'pt-BR' });
    test('wins over the browser language', async ({ page }) => {
      await page.goto('/');
      await expect(page).toHaveURL(/\/pt\/$/);
      await page.locator('a.lang-switch').click();
      await expect(page).toHaveURL(/\/en\/$/);
      await page.goto('/');
      await expect(page).toHaveURL(/\/en\/$/);
    });
  });

  test('a broken saved value falls back to the browser language', async ({ page }) => {
    await page.goto('/pt/');
    await page.evaluate(() => localStorage.setItem('lang', 'klingon'));
    await page.goto('/');
    await expect(page).toHaveURL(/\/en\/$/);
  });

  test('switching languages from a page', async ({ page }) => {
    await page.goto('/pt/');
    await page.locator('a.lang-switch').click();
    await expect(page).toHaveURL(/\/en\/$/);
    await page.goto('/');
    await expect(page).toHaveURL(/\/en\/$/);
  });
});

test('downloads page shows the empty state at launch', async ({ page }) => {
  await page.goto('/pt/downloads/');
  await expect(page.getByText('Ainda não há arquivos para baixar')).toBeVisible();
});

test('CV page hides the phone and serves the PDF', async ({ page, request }) => {
  await page.goto('/pt/curriculo/');
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('João Gabriel de Barros Rocha');
  expect(await page.content()).not.toMatch(BR_PHONE);
  const pdf = await request.get('/cv/cv-pt.pdf');
  expect(pdf.status()).toBe(200);
});

test('unknown pages get the bilingual 404', async ({ page }) => {
  const response = await page.goto('/nao-existe/');
  expect(response?.status()).toBe(404);
  await expect(page.getByText('Página não encontrada')).toBeVisible();
  await expect(page.getByText('Page not found')).toBeVisible();
});

test('mobile navigation shows every section without horizontal scroll', async ({ page }) => {
  await page.goto('/pt/');
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  expect(overflow).toBeLessThanOrEqual(0);
  await expect(page.getByRole('navigation').getByRole('link', { name: 'Currículo' })).toBeVisible();
});
