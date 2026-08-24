# Mapa do Projeto — Rotas Rápidas

> **Arquivo lido pelo PO/Orquestrador.** Mapa de navegação rápida da base de
> conhecimento. Não varrer a base inteira: ir direto ao alvo pela tabela.

## Base de conhecimento (vault)

| O que você quer saber | Onde |
|---|---|
| Visão geral do produto | [01-Visao-Geral/Visao-Geral.md](../01-Visao-Geral/Visao-Geral.md) |
| Problema e objetivo | [02-Problema-Objetivo/Problema-e-Objetivo.md](../02-Problema-Objetivo/Problema-e-Objetivo.md) |
| Escopo (dentro/fora) | [03-Escopo/Escopo.md](../03-Escopo/Escopo.md) |
| Módulos do sistema | [04-Modulos/Modulos.md](../04-Modulos/Modulos.md) |
| Requisitos funcionais (RF) | [05-Requisitos-Funcionais/Requisitos-Funcionais.md](../05-Requisitos-Funcionais/Requisitos-Funcionais.md) |
| Requisitos não funcionais (RNF) | [06-Requisitos-Nao-Funcionais/Requisitos-Nao-Funcionais.md](../06-Requisitos-Nao-Funcionais/Requisitos-Nao-Funcionais.md) |
| Regras de negócio (RN) | [07-Regras-Negocio/Regras-Negocio.md](../07-Regras-Negocio/Regras-Negocio.md) |
| Casos de uso | [08-Casos-Uso/Casos-Uso.md](../08-Casos-Uso/Casos-Uso.md) |
| Fluxos de sistema (diagrama) | [09-Fluxos-Sistema/Fluxos-Sistema.excalidraw.md](../09-Fluxos-Sistema/Fluxos-Sistema.excalidraw.md) |
| Dashboards e indicadores | [10-Dashboard-Indicadores/Dashboard-Indicadores.md](../10-Dashboard-Indicadores/Dashboard-Indicadores.md) |
| Integração Mercado Livre | [11-Integracao-Mercado-Livre/Integracao-Mercado-Livre.md](../11-Integracao-Mercado-Livre/Integracao-Mercado-Livre.md) |
| Critérios de aceitação | [12-Criterios-Aceitacao/Criterios-Aceitacao.md](../12-Criterios-Aceitacao/Criterios-Aceitacao.md) |
| Matriz de rastreabilidade | [13-Matriz-Rastreabilidade/Matriz-Rastreabilidade.md](../13-Matriz-Rastreabilidade/Matriz-Rastreabilidade.md) |
| Pendências e decisões em aberto | [14-Pendencias/Pendencias.md](../14-Pendencias/Pendencias.md) |
| Kanban de desenvolvimento (backlog + sprints) | [15-Desenvolvimento/Kanban-Desenvolvimento.kanban.md](../15-Desenvolvimento/Kanban-Desenvolvimento.kanban.md) |

## Arquitetura e referências (ARQUITETURA)

| O que você quer saber | Onde |
|---|---|
| Stack e decisões técnicas | [ARQUITETURA/01-stack.md](../ARQUITETURA/01-stack.md) |
| Arquitetura (modular monolith, outbox, eventos) | [ARQUITETURA/02-arquitetura.md](../ARQUITETURA/02-arquitetura.md) |
| Diagrama da stack | [ARQUITETURA/02-stack-diagrama.excalidraw.md](../ARQUITETURA/02-stack-diagrama.excalidraw.md) |
| Diagrama da arquitetura | [ARQUITETURA/03-arquitetura-diagrama.excalidraw.md](../ARQUITETURA/03-arquitetura-diagrama.excalidraw.md) |
| Referências e bibliotecas (versões, uso) | [ARQUITETURA/Referencias/bibliotecas.md](../ARQUITETURA/Referencias/bibliotecas.md) |
| Índice de referências / setup de contas | [ARQUITETURA/Referencias/README.md](../ARQUITETURA/Referencias/README.md) |
| Análise do projeto (visão geral) | [15-Desenvolvimento/Analise-Projeto.md](../15-Desenvolvimento/Analise-Projeto.md) |

## Código (repo) — para o Tech Lead

| Pasta | Stack | Comando de validação |
|---|---|---|
| `frontend/` | React 19 + TS + Vite + Tailwind/shadcn + react-query/axios | `npm run lint` e `npm run build` |
| `backend/` | Java (JDK 25 LTS) + Spring Boot 4.0.7 + Modulith (Maven) | `.\mvnw.cmd test` (Windows) / `./mvnw test` |
| `ingestion/` | Go (Kafka, webhooks ML, sync) | `go build ./...` e `go test ./...` |
| `infra/` | Docker Compose + Terraform | `docker compose up -d` |

## Tabela de decisão rápida

| Usuário pergunta sobre… | Abrir direto |
|---|---|
| Regra de negócio | `07-Regras-Negocio` |
| Requisito funcional | `05-Requisitos-Funcionais` |
| Integração Mercado Livre | `11-Integracao-Mercado-Livre` |
| Status do desenvolvimento | `15-Desenvolvimento` (kanban) |
| Decisões pendentes | `14-Pendencias` |
| Stack / por que tecnologia X | `ARQUITETURA/01-stack.md` |
| Arquitetura / padrões | `ARQUITETURA/02-arquitetura.md` |
| Dúvida sobre biblioteca | `ARQUITETURA/Referencias/bibliotecas.md` |
| Fluxo de negócio ponta a ponta | `09-Fluxos-Sistema` |

## Regras de navegação

- Ler `AGENTS.md` (raiz) e depois este mapa — nada de varrer a base inteira.
- Excalidraw (`.excalidraw.md`): ler a seção `## Text Elements`; o desenho está
  no bloco `## Drawing`.
- Kanban (`.kanban.md`): colunas são `## `, cards são `- [ ]` com
  `label::`/`priority::`.
- Itens `[A DEFINIR]` bloqueiam; `[VALIDAR]` exigem confirmação.