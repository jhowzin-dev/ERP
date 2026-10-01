---
version: 1
status: draft
---

# Tasks — Harness OpenCode Universal

## Legenda
- `[ ]` pendente | `[~]` em andamento | `[x]` concluído | `[-]` cancelado

## P0 — Consertar o chão

- [ ] T-001: Renomear baseline para AGENTS.baseline.md e validar que apenas um AGENTS.md é sempre-on (~1h)
- [ ] T-002: Substituir todas refs `.claude/` → `.opencode/` em agents, skills e DOCS (~2h)
- [ ] T-003: Remover leftovers EF/DbContext/AsNoTracking/xUnit/Cucumber de agents/skills (~2h)
- [ ] T-004: Garantir cobertura ingestion/ em debug/test/performance agents (~1h)
- [ ] T-005: Criar `evals/evals.json` com 12 casos de roteamento e Goal Gate (~3h)
- [ ] T-006: Corrigir `run_eval.py` default path para `evals/evals.json` e remover `evals/evals/evals.json` (~1h)
- [ ] T-007: Criar ou remover skill `frontend-design` conforme tabela AGENTS.md (~1h)

## P1 — OpenCode core

- [ ] T-008: Encurtar `opencode.json` instructions para AGENTS.md apenas (~1h)
- [ ] T-009: Criar ficheiros orchestrator.md/plan.md/build.md em `.opencode/agents` alinhados ao JSON (~2h)
- [ ] T-010: Validar runner com modelos NVIDIA via OpenCode (~1h)

## P2 — Qualidade de prompt/skills

- [ ] T-012: Compactar AGENTS.md para <150 linhas com tabela roteamento e gates (~2h)
- [ ] T-013: Atualizar descriptions YAML das skills para trigger curto (~2h)
- [ ] T-014: Remover duplicação de AGENTS.md em meta-agent e sdd-orchestrator (~1h)
- [ ] T-015: Adicionar casos positivos/negativos para `run_trigger_eval.py` (~2h)

## P3 — Medir e fechar loop

- [ ] T-016: Rodar baseline de evals e gerar `evals/results.json` (~1h)
- [ ] T-017: Configurar `eval-viewer` e gerar `evals/review.html` (~1h)
- [ ] T-018: Documentar Safety Rail `--adopt` com delta de pass rate (~1h)

## Dependências
T-005 depende de T-002
T-010 depende de T-009
T-012 depende de T-008
