---
name: frontend-skill
description: Convenções React/TypeScript/Vite/Tailwind do OminiCore. Componentes, react-query, SCSS Modules, auth/RBAC. Leitura obrigatória antes de escrever código frontend.
---

# Frontend Skill — Convenções React/Vite/Tailwind

> Skill de conhecimento para agents frontend. Ler antes de escrever código em `frontend/`.

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

## Convenções

- Componentes em `PascalCase` (arquivo e export)
- Hooks em `camelCase` com prefixo `use`
- Services em `camelCase` (arquivo) com exports nomeados
- SCSS Modules para estilos (`*.module.scss`)
- i18n para todos os textos visíveis
- `any` proibido — respostas da API entram como `unknown` e passam por `schema.parse`

## Validações

```bash
cd frontend && npm run lint
cd frontend && npm run build
.\harness.ps1 frontend        # Harness completo
```

