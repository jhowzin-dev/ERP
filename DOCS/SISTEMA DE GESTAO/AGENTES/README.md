# AGENTES — Runbook de Engenharia com Agentes

> Pasta com o runbook do sistema de agentes especializados do SG-MULTIDIA
> (4 de execução + QA + Documentador).
> Este é o **guia de instruções** (estilo `AGENTS.md`), não código executável.

## Como usar

A hierarquia é operada seguindo os documentos abaixo, em ordem. Cada etapa lê a
saída da anterior e a transforma:

```
Você (pedido) ──► PO.md ──► TECH_LEAD.md ──► DEV_FRONT.md / DEV_BACK.md ──► QA.md
                     │            │                   │                     │
                     │  lê o vault │  define arquivos  │  implementa         │  roda harness
                     │  e divide   │  exatos           │  + teste local      │  + critérios de aceite
                     └─────────────┴───────────────────┴─────────────────────┴──► PASS/FAIL

Você (pedido de doc) ──► DOCS.md ──► melhora a documentação do vault
                              (seção por seção, com sua aprovação)
```

## Índice

| Arquivo | Papel | Escreve código? |
|---------|-------|-----------------|
| [PO.md](PO.md) | PO / Orquestrador / Cérebro — entende produto, define regras de negócio e cria a tarefa dividida | ❌ Não |
| [TECH_LEAD.md](TECH_LEAD.md) | Tech Lead / Arquiteto — plano técnico, arquitetura e lista exata de arquivos | ❌ Não |
| [DEV_FRONT.md](DEV_FRONT.md) | Dev Frontend — UI, componentes e páginas (só `frontend/`) | ✅ Sim |
| [DEV_BACK.md](DEV_BACK.md) | Dev Backend — APIs, banco e regras no servidor (`backend/` + `ingestion/`) | ✅ Sim |
| [QA.md](QA.md) | QA / Gate de qualidade — valida build, testes e critérios de aceite | ❌ Não |
| [DOCS.md](DOCS.md) | Documentador / Technical Writer — melhora clareza, estrutura e links da doc | ❌ Não |
| [mapa-projeto.md](mapa-projeto.md) | Mapa de rotas rápidas do vault (o que o PO lê primeiro) | ❌ Não |
| [tarefa.md](tarefa.md) | Template de handoff estruturado entre os agentes | ❌ Não |
| [fluxo-agentes.md](fluxo-agentes.md) | Protocolo completo da hierarquia e handoff | ❌ Não |

## Regras transversais (vale para todos)

- Ler `AGENTS.md` (raiz do repo) antes de qualquer coisa.
- Não inventar requisitos. Marcadores `[A DEFINIR]` (bloqueia) e `[VALIDAR]`
  (risco) vêm de `14-Pendencias/Pendencias.md`.
- Devs devem rodar o harness antes de concluir; a aprovação final é do QA.
- Nunca tocar em `.excalidraw.md`/`.kanban.md` fora de atualizações deliberadas
  (manter frontmatter e bloco `## Drawing` intactos).
- **Modo rápido**: perguntas informativas ou pequenos ajustes de doc não passam
  pelo pipeline — responder direto (ver `fluxo-agentes.md`).

## Harness de validação

Scripts executáveis na raiz do repositório:

- `harness.ps1` — Windows (PowerShell 5.1+)
- `harness.sh` — Linux/macOS/CI

Uso: `.\harness.ps1` (todos) ou `.\harness.ps1 frontend` / `backend` / `ingestion`.
Sai com exit code `0` se tudo passou, `1` se alguma etapa falhou, `2` se o módulo for inválido.

**Ambiente antes de rodar:** backend testa contra Postgres real — subir
`docker compose up -d` em `infra/`; `ingestion` exige Go instalado.