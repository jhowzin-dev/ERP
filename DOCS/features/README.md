# Features — Especificações por Feature

> Convenção para specs de feature neste monorepo. Cada feature vive em
> `docs/features/<feature-id>/` e contém os 4 artefatos do fluxo SDD.

## Estrutura esperada

```
docs/features/<feature-id>/
├── prd.md        ← Product Requirements Document (fase A)
├── design.md     ← Design técnico / arquitetura (fase B)
├── spec.md       ← Especificação detalhada + contrato de dados (fase C)
├── tasks.md      ← Lista de tarefas quebradas por executável (fase D)
└── state.md      ← Estado atual da feature (em progresso, done, blocked)
```

## Convencões

- `<feature-id>` usa `kebab-case` (ex.: `ml-integration`, `dashboard`, `catalog-sync`).
- Cada arquivo tem `frontmatter` com versão e status:
  ```yaml
  ---
  version: 1
  status: draft | in-review | approved | implementing | done
  ---
  ```
- `state.md` é atualizado a cada gate de fase — é o **status vivo** da feature.
- Não inventar requisitos: usar `[A DEFINIR]` (bloqueia) e `[VALIDAR]` (risco).

## Features ativas

| Feature | Escopo MVP | Status |
|---------|-----------|--------|
| [ml-integration](ml-integration/) | Publicação de produtos no ML, sync estoque/preço, webhooks de pedidos | `draft` |
| [dashboard](dashboard/) | Dashboard de gestão: KPIs, visão de vendas, estoque, pedidos | `draft` |

## Fluxo SDD (resumo)

1. **PRD** (`prd.md`): o quê e por quê — problema, personas, funcionalidades, métricas de sucesso.
2. **Design** (`design.md`): como — arquitetura, diagramas, tecnologias, decisões técnicas.
3. **Spec** (`spec.md`): contrato exato — endpoints, DTOs, schemas, regras de validação, testes.
4. **Tasks** (`tasks.md`): o que executar — tarefas quebradas, dependências, estimativas.

> O orchestrator completo está em `../sdd/SDD-ORCHESTRATOR.md`.
