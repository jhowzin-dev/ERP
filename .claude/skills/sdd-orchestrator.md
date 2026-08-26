---
name: sdd-orchestrator
description: Fluxo Spec-Driven Development: PRD → design → spec → tasks com gate humano por fase. Use para features novas que precisam de planejamento completo antes do código.
---

# SDD Orchestrator

> Executor do fluxo Spec-Driven Development. Cada fase tem um gate humano
> antes de avançar.

## Fluxo

```
Fase A (PRD) ──gate──► Fase B (Design) ──gate──► Fase C (Spec) ──gate──► Fase D (Tasks) ──gate──► Fase E
```

## Arquivos de saída

Cada feature vive em `docs/features/<feature-id>/`:

| Fase | Arquivo | Quem executa |
|------|---------|-------------|
| A | `prd.md` | PO |
| B | `design.md` | java-architect |
| C | `spec.md` | java-architect + implementers |
| D | `tasks.md` | java-architect |
| E | código | implementers |

## Gates

Cada fase tem critérios de gate validados antes de avançar. O gate é **humano** — o orchestrator não aprova automaticamente.

## Detalhes completos

Ver `docs/sdd/SDD-ORCHESTRATOR.md` para templates, critérios de gate e fluxo detalhado.
