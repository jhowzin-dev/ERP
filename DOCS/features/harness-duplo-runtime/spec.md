---
version: 1
status: draft
---

# Spec — Harness Duplo Runtime

## 1. Contrato de dados

### evals/evals.json
```json
{
  "evals": [
    {
      "id": "string",
      "task": "string",
      "runtime": "opencode|cursor|both",
      "expected": {
        "expect_agent": "string",
        "expect_no_edit": true,
        "expect_files": ["string"],
        "expect_exit_0": true,
        "forbidden_substrings": ["string"]
      }
    }
  ]
}
```

### Agent file template `.opencode/agents/<name>.md`
Frontmatter + seções: Papel, Gatilhos, Skills Obrigatórias, Processo, Regras Invioláveis, Critérios de Aceite, Goal Gate.

## 2. Endpoints
N/A — alteração de arquivos estáticos.

## 3. Regras de validação
- `grep -r "\.claude/" .opencode` → 0 ocorrências.
- `wc -l AGENTS.md` < 150.
- Baseline filename != `AGENTS.md`.
- `evals/evals.json` existe e contém ≥12 casos.
- `run_eval.py` default path = `evals/evals.json`.
- Skills descriptions via YAML `description:` curta.

## 4. Regras de negócio
- AGENTS.md curto nunca contém corpo de skill.
- Orquestrador não edita código produto.
- Evals não usam heurística 60%; usar asserts estruturados.
- Runner dual suporta `--runtime opencode|cursor`.

## 5. Testes
- Teste de roteamento: prompt "Revisar PR backend" → expect_agent `code-reviewer`.
- Teste de path: skill SKILL.md contém path `.opencode/skills/...`.
- Teste de Goal Gate: tarefa de implementação termina com comando Maven/NPM/Go exit 0.
- Teste de não-regressão: `git diff --name-only` vazio para agentes read-only.
