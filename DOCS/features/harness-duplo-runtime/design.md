---
version: 1
status: draft
---

# Design — Harness OpenCode Universal

## 1. Visão técnica
Unificar a fonte de verdade em `.opencode/agents` e `.opencode/skills` para OpenCode apenas. Evals tornam-se spec executável com asserts estruturados, compatível com qualquer modelo LLM via OpenCode.

## 2. Arquitetura
- **Source of Truth**: `.opencode/agents/*.md`, `.opencode/skills/*/SKILL.md`
- **OpenCode Adapter**: `opencode.json` com `instructions → AGENTS.md` apenas, permissions existentes.
- **Evals**: `evals/evals.json` + `evals/scripts/` (run_eval, run_loop) com asserts estruturados.
- **Docs**: `docs/` atualizado para refletir paths `.opencode`.

Diagrama:
```
.opencode/ --> OpenCode opencode.json --> Agent file
evals/ --> runner --> asserts
```

## 3. Tecnologias envolvidas
- OpenCode core
- Python 3.11 scripts evals
- Git grep para validação de paths

## 4. Diagrama de componentes
- Orchestrator → lê AGENTS.md curto → carrega agent file → delega via Task
- Agent files → referenciam skill SKILL.md em `.opencode/skills`
- Evals runner → executa prompts, verifica expect_agent / expect_no_edit / expect_exit_0
- Baseline: `AGENTS.baseline.md` fora do always-on

## 5. Decisões técnicas
- Não duplicar conteúdo de skills em AGENTS.md.
- AGENTS.md curto <150 linhas.
- Baseline renomeado para não ser sempre aplicado.
- Asserts estruturados substituem heurística 60% keywords.
- Compatível com qualquer modelo LLM via OpenCode.

## 6. Riscos técnicos
- Baseline ainda injectado se renomeio falhar → mitigar com teste grep.
- Path mortos escondidos em DOCS → mitigar com grep recursivo.
- Evals dependem de `opencode run` → garantir execução com modelos NVIDIA via OpenCode.
