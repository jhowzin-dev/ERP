# OminiCore - Contexto de desenvolvimento

Antes de implementar ou desenhar mudanças significativas, alinha-te ao **Spec-Driven Development** e à arquitectura descrita no repositório.

## Monorepo

| Pasta | Tecnologia |
|-------|-----------|
| `backend/` | Java 21, Spring Boot 4.0.7, Spring Modulith (Maven) |
| `frontend/` | React 19, Vite 8, Tailwind v4, TypeScript strict |
| `ingestion/` | Go 1.22, kafka-go (webhooks ML, sync estoque/preço) |

Mapa completo de pastas e comandos de build: [`docs/README.md`](docs/README.md)

## Fonte principal - SDD

- **Especificação do produto:** [`docs/sdd/OMINICORE-SDD.md`](docs/sdd/OMINICORE-SDD.md) - princípios, camadas, fases A–E, gates de verificação.
- **Fluxo por feature:** [`docs/sdd/SDD-ORCHESTRATOR.md`](docs/sdd/SDD-ORCHESTRATOR.md) e [`docs/sdd/SDD-USAGE-GUIDE.md`](docs/sdd/SDD-USAGE-GUIDE.md). Artefactos em `docs/features/<feature-id>/`.
- **ADRs:** [`docs/sdd/adrs/`](docs/sdd/adrs/) - decisões estruturais duradouras.
- **Backlog:** [`docs/sdd/FEATURES-BACKLOG.md`](docs/sdd/FEATURES-BACKLOG.md) (quando existir).

## Agentes especialistas (`.claude/agents/`)

Invoca pelo **nome** com a ferramenta Agent (`subagent_type`). Cada agente já traz a sua allowlist de
ferramentas e lê a skill correspondente no arranque — não copies convenções para o prompt de delegação.
Índice e padrão de escrita: [`docs/agents/README.md`](docs/agents/README.md).

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

Orquestração mínima: um especialista quando bastar; cadeias curtas só quando a tarefa exigir.

## Skills (`.claude/skills/`)

Carregadas automaticamente quando a situação encaixa, ou por `/<nome>`. Índice e padrão:
[`docs/skills/README.md`](docs/skills/README.md).

| Área | Skill |
|------|-------|
| Convenções backend Java/Spring (conhecimento) | `backend-skill` |
| Convenções frontend React/Vite/Tailwind (conhecimento) | `frontend-skill` |
| Pedido vago ou multi-domínio → rotear e encadear | `/meta-agent` |
| Especificar feature antes de código (gate por fase) | `/sdd-orchestrator` |
| Regressão E2E pela UI real | `/e2e-qa-skill` |

Orquestração é skill, não agente: um subagente não tem a ferramenta Agent e por isso só conseguiria
recomendar, não delegar.

## Regras de comportamento

- **SDD first:** para features novas ou refactors com contrato negócio/técnico, seguir o fluxo SDD (PRD → design → spec/tasks) antes de gerar código.
- **Human-in-the-loop:** merge e decisões de risco ficam com o humano. Sem secrets no repo.
- **Segurança:** autorização (RBAC) explícita onde o SDD e a feature exigirem; validar inputs na fronteira.
- **Modulith:** dependências entre módulos de negócio apenas via eventos Kafka ou injecção controlada. **Não** criar dependências directas entre módulos diferentes.
- **Frontend:** TypeScript `strict`, sem `any`, Tailwind v4 — não expandir para outro CSS framework.
- **Idioma:** respostas e artefactos em **português (Brasil)**; identificadores de código em inglês.
