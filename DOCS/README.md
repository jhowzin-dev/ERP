# Docs — Processo de Engenharia

> Índice canônico para IA e equipe alinharem ao produto neste monorepo. O contexto sempre aplicável está em [`../AGENTS.md`](../AGENTS.md), na raiz do repositório.

Esta pasta cobre **processo** (SDD, ADRs, agentes, skills, especificações por feature).

## Estrutura

```
docs/
├── README.md                    ← este arquivo
├── agents/                      ← runbook dos agentes (índice)
├── sdd/                         ← Spec-Driven Development
│   ├── SDD-ORCHESTRATOR.md      ← fluxo PRD → design → spec → tasks
│   ├── SDD-USAGE-GUIDE.md       ← templates de prompt, versionamento
│   └── adrs/                    ← Architecture Decision Records
├── features/                    ← specs por feature
│   ├── ml-integration/          ← MVP: Mercado Livre
│   └── dashboard/               ← MVP: Dashboard
└── skills/                      ← índice de skills

.claude/
├── agents/                      ← agent files com frontmatter
└── skills/                      ← skill files (conhecimento + orquestração)
```

## Onde ler primeiro

| Prioridade | Documento | Quando |
|------------|-----------|--------|
| 1 | `../AGENTS.md` | Visão geral do projeto, stack, navegação |
| 2 | `sdd/OMINICORE-SDD.md` | SDD completo: filosofia, visão, pipeline, convenções |
| 3 | `agents/README.md` | Workflow completo dos agentes, harness, regras transversais |
| 4 | `../.claude/skills/backend-skill/SKILL.md` | Convenções Java/Spring/Modulith |
| 5 | `sdd/SDD-ORCHESTRATOR.md` | Fluxo SDD para features novas |

## SDD e especificações por feature

| Documento | Quando usar |
|-----------|-------------|
| `sdd/SDD-ORCHESTRATOR.md` | Fluxo PRD → design → spec/tasks; gate antes de código |
| `sdd/SDD-USAGE-GUIDE.md` | Templates de prompt, versões em frontmatter, state.md |
| `sdd/adrs/README.md` | ADRs transversais (índice dos existentes) |

`features/<feature-id>/` é a convenção para specs por feature (`prd.md`, `design.md`, `spec.md`, `tasks.md`) — ver `features/README.md`.

| Feature | Escopo |
|---------|--------|
| `features/ml-integration/` | Integração Mercado Livre: publicação, sync, webhooks |
| `features/dashboard/` | Dashboard de gestão: KPIs, indicadores, resumo |

## Agentes e Skills

> Ver `agents/README.md` para o workflow completo e padrão de escrita.

| Skill | Tipo | Uso rápido |
|-------|------|-----------|
| `backend-skill` | Conhecimento | Convenções Java/Spring/Modulith |
| `frontend-skill` | Conhecimento | Convenções React/Vite/Tailwind |
| `meta-agent` | Orquestração | Roteia pedido vago ou multi-domínio |
| `sdd-orchestrator` | Orquestração | PRD → design → spec/tasks com gate |
| `e2e-qa-skill` | Conhecimento | Metodologia E2E pela UI real |

## Comandos úteis

```bash
# Backend (exige Postgres rodando: docker compose up -d)
.\mvnw.cmd test              # Windows
./mvnw test                  # Linux/macOS

# Frontend
cd frontend && npm run lint && npm run build

# Ingestion
cd ingestion && go build ./... && go test ./...

# Harness completo (QA gate)
.\harness.ps1                # Windows (todos os módulos)
./harness.sh                 # Linux/macOS
```

## Maintenance Rules

- **agents/**: índice dos agentes. Ver `agents/README.md` para workflow.
- **Preservar** arquivos `.excalidraw.md` e `.kanban.md`.
- **Não inventar requisitos**: usar `[A DEFINIR]` (bloqueia) ou `[VALIDAR]` (risco).

## Secrets & templates

Sem secrets no repo. Copie templates e preencha localmente; em produção, use variáveis de ambiente. Nunca commite chaves, tokens ou senhas.
