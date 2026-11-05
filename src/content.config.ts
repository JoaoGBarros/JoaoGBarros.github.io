import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { isValidTag } from './lib/content';

/** Every entry id is `<slug>/<lang>` (e.g. `here-to-slay/pt`); see src/lib/i18n.ts. */
const idFromPath = ({ entry }: { entry: string }): string =>
  entry.replace(/\.(md|ya?ml)$/, '');

const markdownIn = (base: string) =>
  glob({ base, pattern: '**/{pt,en}.md', generateId: idFromPath });

const tags = z
  .array(
    z.string().refine(isValidTag, {
      message: 'Tags só podem ter letras, números, espaço e _ . + - (sem #, ?, / ou %).',
    }),
  )
  .default([]);

const download = z.object({
  rotulo: z.string(),
  plataforma: z.string(),
  versao: z.string(),
  tamanho: z.string(),
  data: z.coerce.date(),
  url: z.url(),
});

const projetos = defineCollection({
  loader: markdownIn('./src/content/projetos'),
  schema: ({ image }) =>
    z.object({
      titulo: z.string(),
      resumo: z.string(),
      periodo: z.string(),
      stack: z.array(z.string()).default([]),
      tipo: z.enum(['codigo', 'nao-codigo']).default('codigo'),
      repo: z.url().optional(),
      links: z.array(z.object({ rotulo: z.string(), url: z.url() })).default([]),
      destaque: z.number().int().min(1).optional(),
      cor: z
        .string()
        .regex(/^#[0-9a-fA-F]{6}$/)
        .default('#5b5bd6'),
      capa: image().optional(),
      downloads: z.array(download).default([]),
      rascunho: z.boolean().default(false),
    }),
});

const textos = defineCollection({
  loader: markdownIn('./src/content/textos'),
  schema: z.object({
    titulo: z.string(),
    data: z.coerce.date(),
    resumo: z.string(),
    tags,
    projeto: z.string().optional(),
    ordem: z.number().int().optional(),
    fixado: z.boolean().default(false),
    rascunho: z.boolean().default(false),
  }),
});

const feed = defineCollection({
  loader: markdownIn('./src/content/feed'),
  schema: ({ image }) =>
    z
      .object({
        data: z.coerce.date(),
        tags,
        projeto: z.string().optional(),
        imagem: image().optional(),
        imagemAlt: z.string().optional(),
        link: z.url().optional(),
        rascunho: z.boolean().default(false),
      })
      .refine((post) => !post.imagem || Boolean(post.imagemAlt), {
        message: 'Posts com `imagem` precisam de `imagemAlt` (texto alternativo).',
        path: ['imagemAlt'],
      }),
});

const cvItem = z.object({
  titulo: z.string(),
  org: z.string(),
  periodo: z.string(),
  local: z.string().optional(),
  link: z.string().optional(),
  pontos: z.array(z.string()).default([]),
});

const cv = defineCollection({
  loader: glob({
    base: './src/data/cv',
    pattern: '{pt,en}.yaml',
    generateId: idFromPath,
  }),
  schema: z
    .object({
      nome: z.string(),
      cargo: z.string(),
      local: z.string(),
      resumo: z.string(),
      competencias: z.array(z.object({ grupo: z.string(), itens: z.array(z.string()) })),
      experiencias: z.array(cvItem),
      projetos: z.array(cvItem),
      formacao: z.array(cvItem),
      publicacoes: z.array(z.object({ titulo: z.string(), detalhe: z.string() })),
      idiomas: z.string(),
      lideranca: z.array(cvItem),
    })
    .strict(),
});

export const collections = { projetos, textos, feed, cv };
