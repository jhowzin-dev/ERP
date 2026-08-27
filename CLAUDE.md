# OminiCore — Contexto de desenvolvimento

Antes de implementar ou desenhar mudanças significativas, alinha-te à arquitetura descrita no repositório.

## Monorepo

| Pasta | Tecnologia |
|-------|-----------|
| `backend/` | Java 21, Spring Boot 4.0.7, Spring Modulith (Maven) |
| `frontend/` | React 19, Vite 8, Tailwind v4, TypeScript strict |
| `ingestion/` | Go 1.22, kafka-go (webhooks ML, sync estoque/preço) |

Mapa completo de pastas e comandos de build: [`docs/README.md`](docs/README.md)

## Fonte principal — Arquitetura

- **Leia primeiro:** [`docs/sdd/OMINICORE-SDD.md`](docs/sdd/OMINICORE-SDD.md) — SDD completo: filosofia, visão do sistema, pipeline, convenções.
- **Mapa do monorepo:** [`README.md`](README.md) — arquitetura, diagramas, fluxos, setup.
- **ADRs:** [`docs/sdd/adrs/`](docs/sdd/adrs/) — decisões estruturais duradouras.
- **Features:** [`docs/features/`](docs/features/) — specs por feature (ML, Dashboard).

## Agentes especialistas (`.claude/agents/`)

Invoca pelo **nome** com a ferramenta Agent. Cada agente lê a skill correspondente no arranque.
Índice: [`docs/agents/README.md`](docs/agents/README.md).

| Situação | Agente |
|----------|--------|
| Fronteiras / layering / API shape (read-only) | `java-architect` |
| Implementação Java/Spring concreta | `java-implementer` |
| UI / React / Vite / Tailwind | `frontend-engineer` |
| Testes automatizados | `test-engineer` |
| Qualidade de PR / diff (read-only) | `code-reviewer` |
| Bugs / causa raiz | `debug-specialist` |
| Performance com evidência | `performance-optimizer` |
| QA End-to-End (navega a UI real) | `e2e-qa-engineer` |

## Skills (`.claude/skills/`)

Carregadas automaticamente quando a situação encaixa, ou por `/<nome>`.
Índice: [`docs/skills/README.md`](docs/skills/README.md).

| Área | Skill |
|------|-------|
| Convenções backend Java/Spring (conhecimento) | `backend-skill` |
| Convenções frontend React/Vite/Tailwind (conhecimento) | `frontend-skill` |
| Pedido vago ou multi-domínio → rotear e encadear | `/meta-agent` |
| Especificar feature antes de código (gate por fase) | `/sdd-orchestrator` |
| Regressão E2E pela UI real | `/e2e-qa-skill` |

## Regras de comportamento

- **SDD first:** para features novas ou refactors, seguir o fluxo SDD (PRD → design → spec/tasks) antes de gerar código.
- **Human-in-the-loop:** merge e decisões de risco ficam com o humano. Sem secrets no repo.
- **Modulith:** pacotes por domínio (`catalog/`, `marketplace/`, `inventory/`, etc.) com comunicação via eventos Kafka.
- **Frontend:** TypeScript `strict`, sem `any`, Tailwind — não expandir para outro CSS framework.
- **Idioma:** respostas e artefactos em **português (Brasil)**; identificadores de código em inglês.

## Comandos úteis

```bash
# Backend (exige Postgres: docker compose up -d)
.\mvnw.cmd test              # Windows
./mvnw test                  # Linux/macOS

# Frontend
cd frontend && npm run lint && npm run build

# Ingestion
cd ingestion && go build ./... && go test ./...

# Harness completo
.\harness.ps1                # Windows (todos)
.\harness.ps1 backend        # Só backend
./harness.sh                 # Linux/macOS
```

Sem secrets no repo. Copie templates e preencha localmente; em produção, use variáveis de ambiente.

