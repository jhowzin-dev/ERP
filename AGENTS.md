# AGENTS.md — SG-MULTIDIA

Project guide for AI agents. Read this file first, then use the maps below to jump directly to the relevant artifact. Do not scan the entire documentation before answering.

## Project Overview

SG-MULTIDIA is a light, fast management system focused on publishing and managing **products on Mercado Livre** (multi-product catalog, multi-segment — e.g. multimedia / visual-communication / print), with native Mercado Livre (ML) integration. All documentation lives under `DOCS/SISTEMA DE GESTAO/` (Obsidian vault). Two areas:

- `DOCS/SISTEMA DE GESTAO/ARQUITETURA/` — stack, architecture, references and diagrams (implementation/tech)
- `DOCS/SISTEMA DE GESTAO/` (sections `01-…14`) — product requirements (markdown only)
- `DOCS/SISTEMA DE GESTAO/AGENTES/` — agent runbook (PO, Tech Lead, Devs, QA, DOCS)

## Repository Structure

```
ERP/
├── AGENTS.md                    ← this file (only guide in the project)
├── harness.ps1 / harness.sh     validation harness (QA gate)
├── backend/                     Java + Spring Boot 4.x (core ERP)
├── frontend/                    React + TS + Vite (SPA)
├── ingestion/                   Go (ML webhooks, sync, ETL)
├── infra/                       Docker Compose local + Terraform
└── DOCS/SISTEMA DE GESTAO/      Obsidian vault
    ├── 01-Visao-Geral … 14-Pendencias   product sections
    ├── 15-Desenvolvimento/      Kanban + Analise-Projeto
    ├── AGENTES/                 agent runbook (6 agents)
    ├── ARQUITETURA/             stack & architecture (implementation)
    │   ├── 01-stack.md          stack decisions + RNF matrix
    │   ├── 02-arquitetura.md    architecture (modular monolith, outbox, events)
    │   ├── 02-stack-diagrama.excalidraw.md
    │   ├── 03-arquitetura-diagrama.excalidraw.md
    │   └── Referencias/
    │       ├── README.md        index of references
    │       └── bibliotecas.md   official links per technology/library
    ├── 09-Fluxos-Sistema/Fluxos-Sistema.excalidraw.md   business process flow
    └── 15-Desenvolvimento/Kanban-Desenvolvimento.kanban.md  dev board (sprints)
```

## Documentation Map

| Path | Purpose | When to use |
|------|---------|-------------|
| `DOCS/SISTEMA DE GESTAO/ARQUITETURA/01-stack.md` | Stack decisions, layer-by-layer, RNF→tech matrix | Any stack/tech question |
| `DOCS/SISTEMA DE GESTAO/ARQUITETURA/02-arquitetura.md` | Architecture: modular monolith, outbox, events, retry | Architecture/patterns questions |
| `DOCS/SISTEMA DE GESTAO/ARQUITETURA/02-stack-diagrama.excalidraw.md` | Stack overview diagram | Visual stack context |
| `DOCS/SISTEMA DE GESTAO/ARQUITETURA/03-arquitetura-diagrama.excalidraw.md` | Block view of the architecture | Visual architecture context |
| `DOCS/SISTEMA DE GESTAO/ARQUITETURA/Referencias/bibliotecas.md` | Official links, versions, where each lib is used | Doubt about a library/technology |
| `DOCS/SISTEMA DE GESTAO/ARQUITETURA/Referencias/README.md` | Index of references + account setup links | Setup accounts, navigate references |
| `DOCS/SISTEMA DE GESTAO/09-Fluxos-Sistema/Fluxos-Sistema.excalidraw.md` | End-to-end business process flow (no tech) | Process/business flow questions |
| `DOCS/SISTEMA DE GESTAO/15-Desenvolvimento/Kanban-Desenvolvimento.kanban.md` | Dev backlog, sprints, priorities, status | Dev status, what's planned/in progress |
| `DOCS/SISTEMA DE GESTAO/14-Pendencias/Pendencias.md` | Open decisions `[A DEFINIR]`, validations `[VALIDAR]` | Pending decisions/risks |
| `DOCS/SISTEMA DE GESTAO/0X-*/…` | Vault sections: Escopo, Módulos, RF, RNF, RN, Casos de Uso, Dashboards, Matriz, etc. | Product requirements detail |

## Quick Decision Table

| User asks about… | Open directly |
|---|---|
| Stack, technologies, why X | `DOCS/SISTEMA DE GESTAO/ARQUITETURA/01-stack.md` |
| Doubt about a library / official docs | `DOCS/SISTEMA DE GESTAO/ARQUITETURA/Referencias/bibliotecas.md` |
| Architecture, patterns (outbox, events, retry) | `DOCS/SISTEMA DE GESTAO/ARQUITETURA/02-arquitetura.md` |
| Business process / end-to-end flow | `DOCS/SISTEMA DE GESTAO/09-Fluxos-Sistema/Fluxos-Sistema.excalidraw.md` |
| Dev status, sprint, tasks | `DOCS/SISTEMA DE GESTAO/15-Desenvolvimento/Kanban-Desenvolvimento.kanban.md` |
| Requirements (RF), non-functional (RNF), rules (RN) | `DOCS/SISTEMA DE GESTAO/05-Requisitos-Funcionais/` `06-Requisitos-Nao-Funcionais/` `07-Regras-Negocio/` |
| Mercado Livre integration details | `DOCS/SISTEMA DE GESTAO/11-Integracao-Mercado-Livre/Integracao-Mercado-Livre.md` |
| Pending decisions / open points | `DOCS/SISTEMA DE GESTAO/14-Pendencias/Pendencias.md` |

## Navigation Rules

- Read this file, then jump directly to the target artifact from the map/table above.
- Do not scan the whole documentation set before responding — go straight to the relevant file.
- If the target is an Excalidraw file (`.excalidraw.md`), read the `## Text Elements` section for content; the JSON drawing is inside the `Drawing` code block.
- If the target is a Kanban file (`.kanban.md`), columns are `## ` headings and cards are `- [ ]` items with `label::`/`priority::` metadata.
- Mark unknown or unconfirmed items with `[A DEFINIR]` (blocks) or `[VALIDAR]` (risk) — never invent requirements.

## Maintenance Rules

- **ARQUITETURA/**: implementation/tech docs — stack, architecture, references, diagrams. Keep diagrams as `.excalidraw.md` (native plugin format) and update the markdown docs alongside.
- **SISTEMA DE GESTAO/**: product-only docs (what the system does, not how it's built). No architecture, DB, APIs, infra, or deploy details here.
- **AGENTES/**: runbook of the 6 specialized agents (PO, Tech Lead, Devs, QA, DOCS) + navigation map (`mapa-projeto.md`). Read `AGENTES/README.md` for the workflow.
- Preserve existing `.excalidraw.md` and `.kanban.md` files — do not convert them to plain markdown.
- When updating a diagram, keep the `excalidraw-plugin: parsed` frontmatter and the `## Drawing` code block intact.
- When adding references, use official links and record version + where it is used.
- Keep this file small — it is loaded on every session start.