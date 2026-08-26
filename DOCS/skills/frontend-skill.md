# Frontend Skill — Convenções React/Vite/Tailwind

> Skill de conhecimento para o Dev Frontend. Ler antes de escrever código no `frontend/`.

## Contexto obrigatório

SPA React 19 + TypeScript (strict) + Vite + Tailwind CSS v4.
State management via react-query + axios. Formulários via react-hook-form + zod.

## Stack

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| React | 19 | UI |
| TypeScript | strict | Tipagem |
| Vite | (latest) | Bundler |
| Tailwind CSS | v4 | Estilos |
| React Router | v7 | Rotas |
| TanStack Query | 5 | State do servidor |
| Axios | 1.x | HTTP client |
| React Hook Form | 7 | Formulários |
| Zod | 4 | Validação |
| react-i18next | 17 | i18n |
| oxlint | — | Linter |

## Estrutura

```
frontend/src/
├── main.tsx
├── App.tsx
├── components/       # Componentes compartilhados
├── pages/            # Páginas (rotas)
├── hooks/            # Hooks customizados
├── services/         # Chamadas API
├── types/            # Tipos TypeScript
└── utils/            # Utilitários
```

## Convenções

- Componentes em `PascalCase` (arquivo e export)
- Hooks em `camelCase` com prefixo `use`
- Services em `camelCase` (arquivo) com exports nomeados
- Tipos em `PascalCase` em `types/`
- Usar aliases de import (ver `tsconfig.json`)
- SCSS Modules para estilos (`*.module.scss`)
- i18n para todos os textos visíveis

## Validações

```bash
cd frontend && npm run lint    # Lint
cd frontend && npm run build  # Build
.\harness.ps1 frontend        # Harness completo
```

## Referências

- [`README.md`](../../README.md) — convenções do projeto
- [`docs/sdd/`](../sdd/) — SDD e decisões arquiteturais
