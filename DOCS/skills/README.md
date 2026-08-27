# Skills — Índice

> Skills carregam conhecimento do projeto (convenções, padrões, decisões) e são
> invocadas por agents ou pela thread principal. Não escrevem código — apenas
> informam quem escreve.

## Índice

| Skill | Tipo | Arquivo | Uso rápido |
|-------|------|---------|-----------|
| `backend-skill` | Conhecimento | [`backend-skill/SKILL.md`](../../.claude/skills/backend-skill/SKILL.md) | Convenções Java/Spring/Modulith: camadas, Flyway, Kafka, contrato HTTP, testes |
| `frontend-skill` | Conhecimento | [`frontend-skill/SKILL.md`](../../.claude/skills/frontend-skill/SKILL.md) | Convenções React/Vite/Tailwind: componentes, react-query, SCSS, auth/RBAC |
| `meta-agent` | Orquestração | [`meta-agent/SKILL.md`](../../.claude/skills/meta-agent/SKILL.md) | Roteia pedido vago ou multi-domínio para o especialista certo |
| `sdd-orchestrator` | Orquestração | [`sdd-orchestrator/SKILL.md`](../../.claude/skills/sdd-orchestrator/SKILL.md) | PRD → design → spec/tasks com gate humano por fase |
| `e2e-qa-skill` | Conhecimento | [`e2e-qa-skill/SKILL.md`](../../.claude/skills/e2e-qa-skill/SKILL.md) | Metodologia de testes E2E pela UI real |

## Como funcionam

- **Conhecimento**: lidas pelo agent no arranque (via `Read`). Contêm convenções, padrões, decisões. Nunca recopiadas — cada agent declara `## Contexto obrigatório` e lê a skill.
- **Orquestração**: roteiam pedidos complexos para o especialista certo. Rodam na thread principal (um subagent não tem acesso à ferramenta `Agent`).

## Regra

> Nenhum agent repete convenções que já estão numa skill.
> Cada agent declara `## Contexto obrigatório` com o caminho da skill e **lê** esse arquivo no arranque.
