# SG-MULTIDIA

Sistema de gestão leve e rápido para **publicação de produtos no Mercado Livre e gestão de catálogo multi-produto**, com informações completas por produto e integração nativa ao ML. Atende segmentos diversos (ex.: multimídia, comunicação visual, impressão) e outros modelos de produto.

## Estrutura do repositório

| Pasta | Conteúdo |
|-------|----------|
| `backend/` | Core ERP — Java (JDK 25 LTS) + Spring Boot 4.x + Spring Modulith |
| `ingestion/` | Ingestão/ETL — Go (Kafka consumer, webhooks ML, sync estoque/preço) |
| `frontend/` | SPA — React + TypeScript + Vite + Tailwind/shadcn |
| `infra/` | Docker Compose local + Terraform (AWS) |
| `DOCS/SISTEMA DE GESTAO/` | Documentação de produto (Obsidian vault — 14 seções + AGENTES + ARQUITETURA) |
| `AGENTS.md` | Guia de navegação para IAs (leia antes de qualquer tarefa) |
| `harness.ps1` / `harness.sh` | Harness de validação (QA gate: lint/build/testes) |

## Começando

Pré-requisitos: JDK 25+, Node 20+, Docker Desktop (Go e Terraform opcionais por enquanto).

```bash
# Backend (Java/Spring) — usar o wrapper do projeto
cd backend
.\mvnw.cmd spring-boot:run   # Windows
./mvnw spring-boot:run       # Linux/macOS
# (alternativa: `mvn spring-boot:run` se tiver Maven instalado)

# Frontend (React)
cd frontend
npm install
npm run dev

# Serviços locais (Postgres, Redis, Kafka) — compose está em infra/docker/
docker compose -f infra/docker/docker-compose.yml up -d
```

Acesse o frontend em `http://localhost:5173` e a API em `http://localhost:8080`.

## Referência rápida

- Stack e decisões: `DOCS/SISTEMA DE GESTAO/ARQUITETURA/01-stack.md`
- Arquitetura: `DOCS/SISTEMA DE GESTAO/ARQUITETURA/02-arquitetura.md`
- Links oficiais das bibliotecas: `DOCS/SISTEMA DE GESTAO/ARQUITETURA/Referencias/bibliotecas.md`
- Board de desenvolvimento: `DOCS/SISTEMA DE GESTAO/15-Desenvolvimento/Kanban-Desenvolvimento.kanban.md`
- Runbook de agentes: `DOCS/SISTEMA DE GESTAO/AGENTES/README.md`

## Status

Fase 1 (MVP) em desenvolvimento — ver board de sprints no kanban.