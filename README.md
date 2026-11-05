# jg-website

Site pessoal de João Gabriel de Barros Rocha. Astro + TypeScript, estático, em PT e EN, publicado no GitHub Pages a cada push na `main`.

## Publicar conteúdo

Cada item é uma pasta com um arquivo por idioma (`pt.md`, `en.md`). Se faltar um idioma, o site mostra o outro com um aviso.

| O quê | Onde | Modelo |
|---|---|---|
| Projeto | `src/content/projetos/<slug>/` | `here-to-slay/` |
| Texto longo | `src/content/textos/<slug>/` | `exemplo-serie/` (rascunho) |
| Post curto | `src/content/feed/AAAA-MM-DD-<slug>/` | `2026-11-04-exemplo/` (rascunho) |
| Currículo | `src/data/cv/{pt,en}.yaml` + PDFs em `public/cv/` | — |

- `rascunho: true` esconde o item de tudo (listas, RSS, sitemap).
- Em textos e posts, `projeto: <slug>` liga o item a um projeto. Se o slug não existir (ou for um rascunho), o build falha avisando qual arquivo está errado.
- Tags: letras, números, espaço e `_ . + -`. Use a mesma tag nas duas línguas (ex.: `tecnico`).
- Downloads: preencha `downloads:` no Markdown do projeto, apontando para a GitHub Release. Binários nunca entram neste repositório.
- Telefone: nunca no YAML nem no Markdown. Ele fica só no PDF.

## Comandos

```bash
npm run dev        # servidor local em http://localhost:4321
npm run build      # astro check + build em dist/
npm test           # testes unitários (os de saída do build precisam de dist/)
npm run test:e2e   # Playwright + axe contra o build
```

## Deploy

1. Crie o repositório `JoaoGBarros.github.io` e faça push da `main`.
2. Em **Settings → Pages**, escolha **GitHub Actions** como fonte.
3. Para usar um domínio próprio: troque `site` em `astro.config.mjs` e adicione `public/CNAME`.
