# OminiCore — Spec-Driven Development (SDD)

> **Este é o documento vivo do SDD do OminiCore.**
> Cada feature nova ou refactor significativo passa por este pipeline antes do código.
> O pipeline é **humano-gated** — nenhum agente aprova automaticamente.

---

## 1. Filosofia

O SDD existe porque:

- **Código sem spec gasta retrabalho** — spec antecipa decisões que senão viriam no code review
- **Decisões ficam registradas** — não se pergunta "por que foi feito assim?" depois
- **Testes nascem antes do código** — cobertura nasce da spec, não do chute
- **Agents precisam de contrato** — sem spec, agents inventam convenções inconsistentes

### Princípios

| Princípio | Significado |
| --------- | ----------- |
| **Spec-first** | Código só começa depois que spec está aprovada |
| **Human gate** | Cada fase termina com aprovação humana explícita |
| **Um arquivo por fase** | PRD, design, spec, tasks — cada um vive no seu arquivo |
| **Versões** | Cada artefato tem `version` no frontmatter; incrementa a cada revisão significativa |
| **Append-only** | Nunca editar um ADR aceito; criar novo com `substituído por` |

---

## 2. Visão do Sistema

### Stack

| Camada | Tecnologia |
| ------ | ---------- |
| **Backend** | Java 21, Spring Boot 4.0.7, Spring Modulith, Maven |
| **Frontend** | React 19, Vite 8, Tailwind v4, TypeScript strict |
| **Ingestion** | Go 1.22, kafka-go (webhooks ML, sync estoque/preço) |
| **Banco** | PostgreSQL 15+ |
| **Eventos** | Apache Kafka |
| **Infra** | Docker Compose (dev), CI/CD |

### Arquitetura (C4 - Level 1)

```
┌─────────────────────────────────────────────────────────────┐
│                        Usuário                             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                         │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │Catalog  │ │Inventory│ │  Sales  │ │Dashboard│          │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘          │
└───────┼───────────┼───────────┼───────────┼────────────────┘
        │           │           │           │
        ▼           ▼           ▼           ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend (Spring Boot)                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ catalog  │ │inventory │ │  sales   │ │ finance  │      │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘      │
└───────┼────────────┼────────────┼────────────┼─────────────┘
        │            │            │            │
        ▼            ▼            ▼            ▼
┌─────────────────────────────────────────────────────────────┐
│              PostgreSQL + Kafka (Eventos)                   │
└─────────────────────────────────────────────────────────────┘
```

### Comunicação entre módulos

- **Regra:** Comunicação entre módulos de negócio **apenas via eventos Kafka**
- **Exceção:** injecção controlada via Spring Modulith (quando aprovado no ADR)
- **Proibido:** dependências diretas entre módulos de negócio diferentes

---

## 3. Mapa de Pastas

```
OminiCore/
├── backend/
│   ├── src/main/java/com/ominicore/backend/
│   │   ├── catalog/          # Catálogo de produtos
│   │   │   ├── api/          # Controllers REST
│   │   │   └── internal/     # Services, repositories, entities
│   │   ├── inventory/        # Estoque
│   │   ├── sales/            # Vendas
│   │   ├── finance/          # Financeiro
│   │   ├── customers/        # Clientes
│   │   ├── production/       # Produção
│   │   ├── marketplace/      # Integração ML
│   │   ├── events/           # Eventos cross-domain Kafka
│   │   └── BackendApplication.java
│   ├── src/main/resources/db/migration/  # Flyway
│   └── tests/
├── frontend/
│   └── src/
│       ├── api/services/     # Services de API
│       ├── components/ui/    # Componentes reutilizáveis
│       ├── features/         # Feature modules
│       ├── hooks/            # Custom hooks
│       ├── pages/            # Páginas (rotas)
│       └── types/            # Tipos compartilhados
├── ingestion/
│   └── cmd/                  # Workers Go
├── docs/
│   ├── sdd/                  # Este diretório
│   │   ├── OMINICORE-SDD.md  # Este arquivo
│   │   ├── SDD-ORCHESTRATOR.md
│   │   ├── SDD-USAGE-GUIDE.md
│   │   ├── adrs/             # Architecture Decision Records
│   │   └── requisitos-funcionais/  # Specs de requisitos
│   ├── features/             # Specs por feature
│   ├── agents/               # Índice de agents
│   └── skills/               # Índice de skills
└── .claude/
    ├── agents/               # Agent files
    └── skills/               # Skill files (subpastas)
        ├── backend-skill/SKILL.md
        ├── frontend-skill/SKILL.md
        ├── meta-agent/SKILL.md
        ├── sdd-orchestrator/SKILL.md
        └── e2e-qa-skill/SKILL.md
```

---

## 4. Pipeline SDD — Fases A-E

### Fase A — PRD (Product Requirements Document)

**Quem executa:** PO
**Arquivo:** `docs/features/<feature-id>/prd.md`
**Gate:** Problema claro, personas, funcionalidades com critérios de aceite

### Fase B — Design Técnico

**Quem executa:** java-architect
**Arquivo:** `docs/features/<feature-id>/design.md`
**Gate:** Arquitetura definida, tecnologias validadas, riscos mapeados

### Fase C — Especificação

**Quem executa:** java-architect + implementers
**Arquivo:** `docs/features/<feature-id>/spec.md`
**Gate:** Contrato de dados, endpoints, validações, testes definidos

### Fase D — Tarefas

**Quem executa:** java-architect
**Arquivo:** `docs/features/<feature-id>/tasks.md`
**Gate:** Tarefas executáveis (max ~4h), dependências, estimativas

### Fase E — Implementação

**Quem executam:** java-implementer, frontend-engineer
**Arquivo de referência:** `docs/features/<feature-id>/state.md`
**Gate:** PR pronto para review

---

## 5. Architecture Decision Records (ADRs)

### Template

```markdown
# ADR NNNN: <Título>

**Status**: proposto | aceito | deprecado | substituído por [ADR XXXX](xxxx-titulo.md)
**Data**: YYYY-MM-DD
**Decidido por**: <quem>

## Contexto
<o que está acontecendo que força uma decisão>

## Decisão
<o que decidimos fazer>

## Consequências
<o que fica fácil, o que fica difícil, riscos>

## Alternativas consideradas
<opções avaliadas e por que foram rejeitadas>
```

### Regras

- Toda decisão estrutural nova gera um ADR antes do código
- ADRs são **append-only** — nunca editar um aceito; criar novo
- Decisões de produto vão no vault (`14-Pendencias`), não aqui

---

## 6. Agents e Skills

### Agents (perfis de comportamento)

| Agente | Função |
| ------ | ------ |
| `java-architect` | Fronteiras, API shape, estrutura de módulos |
| `java-implementer` | Código Java de produção |
| `frontend-engineer` | UI React |
| `test-engineer` | Testes automatizados |
| `code-reviewer` | Revisão de diff |
| `debug-specialist` | Causa raiz |
| `performance-optimizer` | Gargalos |
| `e2e-qa-engineer` | QA pela UI real |

### Skills (conhecimento)

| Skill | Conteúdo |
| ----- | -------- |
| `backend-skill` | Convenções Java/Spring/Modulith |
| `frontend-skill` | Convenções React/Vite/Tailwind |
| `meta-agent` | Roteamento de pedidos |
| `sdd-orchestrator` | Fluxo SDD |
| `e2e-qa-skill` | Metodologia E2E |

### Regra de ouro

> Um agent nunca repete no seu prompt o que uma skill já fixa.
> Cada agent declara `## Contexto obrigatório` com o caminho da skill e **lê** esse arquivo.

---

## 7. Convenções Transversais

### Código

| Área | Convenção |
| ---- | --------- |
| **Idioma** | UI e logs em português (Brasil); identificadores em inglês |
| **Backend** | Controllers → Services → Repositories; Bean Validation; camelCase |
| **Frontend** | Components PascalCase; hooks camelCase; SCSS Modules; i18n; sem `any` |
| **Testes** | Unit + Integration; prefixo `_test` ou `_IT` |
| **Banco** | Flyway migrations; soft delete; `isDeleted` + `deletedAt` |
| **Eventos** | Kafka para cross-domain; publicar após commit |

### Git

| Área | Convenção |
| ---- | --------- |
| **Commits** | Conventional Commits (`feat:`, `fix:`, `docs:`) |
| **Branches** | `feature/<feature-id>`, `fix/<issue-id>` |
| **PRs** | Review obrigatório; CI verde antes de merge |
| **Secrets** | Nunca no repo; usar variáveis de ambiente |

---

## 8. Validação

### Comandos de build

```bash
# Backend
.\mvnw.cmd test              # Windows
./mvnw test                  # Linux/macOS

# Frontend
cd frontend && npm run lint && npm run build

# Ingestion
cd ingestion && go build ./... && go test ./...

# Harness completo
.\harness.ps1                # Windows (todos)
./harness.sh                 # Linux/macOS
```

### CI/CD

- Lint + build + testes rodam em todo PR
- Coverage mínimo: 70% (services)
- PR sem CI verde não é mergeável

---

## 9. Referências

| Documento | Caminho |
| --------- | ------- |
| Mapa do monorepo | `docs/README.md` |
| Agents (índice) | `docs/agents/README.md` |
| Skills (índice) | `docs/skills/README.md` |
| ADRs | `docs/sdd/adrs/README.md` |
| Features | `docs/features/README.md` |
| SDD Orchestrator | `docs/sdd/SDD-ORCHESTRATOR.md` |
| SDD Usage Guide | `docs/sdd/SDD-USAGE-GUIDE.md` |

---

## Histórico

| Versão | Data | Mudança |
| ------ | ---- | ------- |
| 1.0.0 | 2026-08-26 | Criação do documento principal SDD |
