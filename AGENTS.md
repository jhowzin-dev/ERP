# OminiCore — Harness OpenCode

Runtime: **OpenCode**. Fonte de verdade: `.opencode/agents/`, `.opencode/skills/`, `opencode.json`.
Não implementar, rever, debugar nem desenhar na thread do `orchestrator` — delegar com a ferramenta Task.

Excepção: pergunta conceitual que não lê nem altera o repositório.

## Roteamento

| Pedido | Agent | Skill |
|--------|-------|-------|
| Revisa diff/PR | `code-reviewer` | skill da camada tocada |
| Infra, Docker, CI/CD, deploy, config | `java-architect` | `backend-skill` |
| Arquitetura, fronteiras Modulith, ADR | `java-architect` | `backend-skill` |
| Código em `backend/` | `java-implementer` | `backend-skill` |
| Código em `frontend/` | `frontend-engineer` | `frontend-skill` |
| Design visual / UI craft | `frontend-engineer` | `frontend-design` |
| Código em `ingestion/` | `go-implementer` | `go-skill` |
| Testes automatizados | `test-engineer` | skill da camada |
| Debug / causa raiz | `debug-specialist` | skill da camada |
| Performance medida | `performance-optimizer` | skill da camada |
| QA pela UI | `e2e-qa-engineer` | `e2e-qa-skill` |
| Feature nova (PRD→código) | thread principal + `sdd-orchestrator` | `sdd-orchestrator` |
| Vago ou multi-domínio | thread principal + `meta-agent` | `meta-agent` |

Antes de Task: identificar agent+skill → ler `.opencode/agents/<agent>.md` → plano em 3–6 passos → delegar com esse contexto.

`build` só se o utilizador invocar esse agent para tarefa trivial mono-domínio.

## Goal Gate

Não declarar concluído sem o comando da camada a verde (exit 0). Máx. 5 tentativas. Logs da última falha no output. Timestamp ISO 8601.

Checklist observável antes de declarar feito:
- [ ] Agent file `.opencode/agents/<agent>.md` foi lido
- [ ] Skill `SKILL.md` foi carregada quando exigida
- [ ] Comando da camada executado com exit 0

| Camada | Comando |
|--------|---------|
| `backend/` | `./mvnw test` ou `.\mvnw.cmd test` (timeout 180s) |
| `frontend/` | `npm run lint && npm run build` em `frontend/` (60s) |
| `ingestion/` | `go build ./... && go test ./...` (60s) |

Saída: `GOAL REACHED` ou `GOAL NOT REACHED` + logs. Re-delegar no máximo 1 vez; depois escalar ao humano.

## Permissões (opencode.json)

Orchestrator não edita código de produto. Reviewers/architect/e2e não escrevem código. Implementers podem editar e correr bash.

## Contexto on-demand

Always-on: este ficheiro. Skills e ADRs: só depois do roteamento. Feature activa: `docs/features/<id>/`.

## Segurança

Sem secrets no git. Config sensível em env. Validar input. Não inventar CVE.

Stack: Java 21 / Spring Boot 4 / Modulith · React 19 / Vite / Tailwind 4 · Go em `ingestion/`.
