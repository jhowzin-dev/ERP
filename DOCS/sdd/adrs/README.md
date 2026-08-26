# ADRs — Architecture Decision Records

> Índice das decisões arquiteturais do SG-MULTIDIA. Cada ADR documenta:
> contexto, decisão, consequências e data.

## Formato

```
docs/sdd/adrs/NNNN-titulo-curto.md
```

Onde `NNNN` é um número sequencial (zero-padded) e `titulo-curto` usa kebab-case.

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

## Índice

| ADR | Título | Status | Data |
|-----|--------|--------|------|
| [ADR-0001](ADR-0001-stack-backend.md) | Stack backend: Java + Spring Boot + Modulith | aceito | 2026-08-01 |
| [ADR-0002](ADR-0002-stack-frontend.md) | Stack frontend: React + Vite + Tailwind | aceito | 2026-08-01 |
| [ADR-0003](ADR-0003-ingestion-go.md) | Ingestão: Go com Kafka | aceito | 2026-08-01 |
| [ADR-0004](ADR-0004-ml-integration.md) | Integração Mercado Livre: webhooks + API REST | proposto | 2026-08-26 |

## Regras

- Toda decisão estrutural nova gera um ADR antes do código
- ADRs são **append-only** — nunca editar um aceito; criar novo com `substituído por`
- Decisões de produto (regras de negócio) vão no vault (`14-Pendencias`), não aqui
