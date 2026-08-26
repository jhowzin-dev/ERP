# AGENTS.md — SG-MULTIDIA

Project guide for AI agents. Read this file first, then use the maps below to jump directly to the relevant artifact. Do not scan the entire documentation before answering.

## Project Overview

SG-MULTIDIA is a light, fast management system focused on publishing and managing **products on Mercado Livre** (multi-product catalog, multi-segment — e.g. multimedia / visual-communication / print), with native Mercado Livre (ML) integration.

## Repository Structure

> Confirma estes paths antes de assumir outros layouts.

| Pasta | Conteúdo típico |
|-------|-----------------|
| `backend/` | API principal Java (Spring Boot 4.0.7, JDK 25, Maven, Spring Modulith). Pacotes por domínio: `finance/`, `sales/`, `inventory/`, `customers/`, `production/`, `marketplace/`, `catalog/`, `events/`. Flyway + JPA + Kafka + Security. |
| `frontend/` | SPA React 19 + TypeScript + Vite + Tailwind v4. Lint: oxlint. State: react-query + axios. Forms: react-hook-form + zod. Routing: react-router-dom v7. i18n: react-i18next. |
| `ingestion/` | Go (Kafka consumer, webhooks ML, sync estoque/preço). Pacote: `cmd/worker/`, `internal/worker/`, `internal/config/`. Lib: kafka-go. |
| `docs/` | SDD, ADRs, skills, especificações por feature, agentes. |
| `.claude/agents/` | Agent files com frontmatter (padrão EmpregaNet). |
| `.claude/skills/` | Skill files (conhecimento + orquestração). |
| `harness.ps1` / `harness.sh` | Scripts de validação (QA gate) — lint, build, test por módulo. |

> **`infra/`** ainda não existe como pasta no repo. Dockerfiles estão em `backend/Dockerfile` e `ingestion/Dockerfile`.

## Where to read first

| Prioridade | Documento | Quando |
|------------|-----------|--------|
| 1 | `DOCS/agents/README.md` | Workflow completo dos agentes, harness, regras transversais |
| 2 | `.claude/agents/java-architect.md` | Convenções de implementação, arquitetura, stack |
| 3 | `.claude/agents/java-implementer.md` | Convenções backend (Java/Spring/Modulith) |
| 4 | `.claude/agents/frontend-engineer.md` | Convenções frontend (React/Vite/Tailwind) |
| 5 | `.claude/skills/backend-skill.md` | Convenções Java/Spring/Modulith |

## Agents

> Invocáveis pelo nome. Padrão de escrita e separação de responsabilidades: `DOCS/agents/README.md`.

| Agente | Responsabilidade | Escrita? |
| ------ | ---------------- | -------- |
| [`java-architect`](.claude/agents/java-architect.md) | Fronteiras de camada, forma da API, estrutura de módulos | Não — read-only |
| [`java-implementer`](.claude/agents/java-implementer.md) | Código Java de produção, com build e testes | Sim |
| [`frontend-engineer`](.claude/agents/frontend-engineer.md) | UI React, com lint, testes e build | Sim |
| [`test-engineer`](.claude/agents/test-engineer.md) | Testes automatizados (xUnit, Cucumber) | Sim, só testes |
| [`code-reviewer`](.claude/agents/code-reviewer.md) | Revisão de diff: corretude, segurança, fronteiras | Não — read-only |
| [`debug-specialist`](.claude/agents/debug-specialist.md) | Causa raiz e correção mínima verificada | Sim |
| [`performance-optimizer`](.claude/agents/performance-optimizer.md) | Gargalos medidos e otimização verificada | Sim |
| [`e2e-qa-engineer`](.claude/agents/e2e-qa-engineer.md) | Regressão pela UI real, via Browser pane | Não altera código |

Orquestração **não** é agente: vive como skill — ver [`DOCS/skills/README.md`](DOCS/skills/README.md).

## Skills

> Carregadas automaticamente pela description, ou invocadas por `/<nome>`.

| Skill | Tipo | Uso rápido |
|-------|------|-----------|
| `backend-skill` | Conhecimento | Convenções Java/Spring/Modulith |
| `frontend-skill` | Conhecimento | Convenções React/Vite/Tailwind |
| `meta-agent` | Orquestração | Roteia pedido vago ou multi-domínio |
| `sdd-orchestrator` | Orquestração | PRD → design → spec/tasks com gate |
| `e2e-qa-skill` | Conhecimento | Metodologia E2E pela UI real |

## Separação de responsabilidades

| Preocupação | Onde vive |
| ----------- | --------- |
| **Orquestração** | skills `meta-agent`, `sdd-orchestrator` |
| **Conhecimento** | skills `backend-skill`, `frontend-skill`, `e2e-qa-skill` |
| **Execução** | agents `java-implementer`, `frontend-engineer`, `test-engineer`, `debug-specialist`, `performance-optimizer` |
| **Validação** | agents `code-reviewer`, `java-architect`, `e2e-qa-engineer` |

## Documentation Map

| Path | Conteúdo | Quando usar |
|------|----------|-------------|
| `DOCS/agents/README.md` | Índice dos agentes, harness, regras transversais | Qualquer tarefa de engenharia |
| `DOCS/sdd/SDD-ORCHESTRATOR.md` | Fluxo PRD → design → spec/tasks; gate antes de código | Nova feature SDD |
| `DOCS/sdd/adrs/README.md` | ADRs transversais (índice dos existentes) | Decisões arquiteturais |
| `DOCS/features/README.md` | Convenção de specs por feature | Criar nova feature spec |
| `DOCS/features/ml-integration/` | Integração Mercado Livre: publicação, sync, webhooks | MVP — marketplace |
| `DOCS/features/dashboard/` | Dashboard de gestão: KPIs, indicadores, resumo | MVP — dashboard |
| `DOCS/skills/README.md` | Índice de skills | Invocar skill |

## Quick Decision Table

| Usuário pergunta sobre… | Abrir direto |
|---|---|
| Pipeline de agentes / como começar | `DOCS/agents/README.md` |
| Arquitetura / padrões | `.claude/agents/java-architect.md` |
| Implementação backend | `.claude/agents/java-implementer.md` |
| Implementação frontend | `.claude/agents/frontend-engineer.md` |
| Validação / QA | `.claude/agents/e2e-qa-engineer.md` |
| Revisão de código | `.claude/agents/code-reviewer.md` |
| Debug | `.claude/agents/debug-specialist.md` |
| Performance | `.claude/agents/performance-optimizer.md` |
| SDD / fluxo de specs | `DOCS/sdd/SDD-ORCHESTRATOR.md` |
| Integração ML (MVP) | `DOCS/features/ml-integration/` |
| Dashboard (MVP) | `DOCS/features/dashboard/` |
| Convenções backend | `.claude/skills/backend-skill.md` |
| Convenções frontend | `.claude/skills/frontend-skill.md` |

## Navigation Rules

- Read this file, then jump directly to the target artifact from the map/table above.
- Do not scan the whole documentation set before responding — go straight to the relevant file.
- Mark unknown or unconfirmed items with `[A DEFINIR]` (blocks) or `[VALIDAR]` (risk) — never invent requirements.
- **Modo rápido**: perguntas informativas ou pequenos ajustes de doc não passam pelo pipeline — responder direto.

## Useful commands

> Comandos de verificação local. Rodar na raiz do repositório.

```bash
# Backend (exige Postgres rodando: docker compose up -d em infra/)
.\mvnw.cmd test              # Windows
./mvnw test                  # Linux/macOS

# Frontend
cd frontend && npm run lint && npm run build

# Ingestion
cd ingestion && go build ./... && go test ./...

# Harness completo (QA gate)
.\harness.ps1                # Windows (todos os módulos)
.\harness.ps1 backend        # Windows (só backend)
./harness.sh                 # Linux/macOS
```

## Maintenance Rules

- **Agent files**: follow pattern in `DOCS/agents/README.md` (frontmatter + body sections).
- **Preservar** arquivos `.excalidraw.md` (frontmatter `excalidraw-plugin: parsed` + bloco `## Drawing`) e `.kanban.md` (frontmatter + blocos `%% kanban:settings %%`).
- **Não inventar requisitos**: itens novos exigem `[A DEFINIR]` (bloqueia) ou `[VALIDAR]` (risco).
- Keep this file small — it is loaded on every session start.

## Secrets & templates

Sem secrets no repo. Copie templates e preencha localmente; em produção, use variáveis de ambiente. Nunca commite chaves, tokens ou senhas.
