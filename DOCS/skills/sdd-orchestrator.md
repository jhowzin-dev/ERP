# SDD Orchestrator Skill

> Executor do fluxo Spec-Driven Development. Invocado como skill, não como agente.
> Detalhes completos: `docs/sdd/SDD-ORCHESTRATOR.md`.

## Resumo do fluxo

```
Fase A (PRD) ──gate──► Fase B (Design) ──gate──► Fase C (Spec) ──gate──► Fase D (Tasks) ──gate──► Fase E
```

## Como invocar

```
/sdd-orchestrator
```

Ou pela `description`: quando o pedido for uma feature nova que precisa de PRD → design → spec → tasks.

## Gate por fase

Cada fase tem critérios de gate que o orchestrator valida antes de gerar o template da próxima fase. O gate é **humano** — o orchestrator não aprova automaticamente.

## Templates

Os templates de cada fase estão em `docs/sdd/SDD-ORCHESTRATOR.md`. Os arquivos de saída ficam em `docs/features/<feature-id>/`.
