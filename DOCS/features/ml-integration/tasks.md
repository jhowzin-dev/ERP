---
version: 1
status: draft
---

# Tasks — Integração Mercado Livre

## Legenda

- `[ ]` pendente | `[~]` em andamento | `[x]` concluído | `[-]` cancelado

## Backend (Java/Spring)

- [ ] T-001: Entidade `MLPublication` + migration (product_id, ml_item_id, status, last_sync) (~2h)
- [ ] T-002: Entidade `MLToken` + migration (access_token, refresh_token, expires_at, user_id) (~2h)
- [ ] T-003: Repository `MLPublicationRepository` + `MLTokenRepository` (~1h)
- [ ] T-004: Service `MLAuthService` — refresh token automático (~3h)
- [ ] T-005: Service `MLPublicationService` — publicar/despublicar produto (~4h)
- [ ] T-006: Service `MLSyncService` — sync de estoque/preço (~3h)
- [ ] T-007: Service `MLOrderService` — criar pedido a partir de webhook (~3h)
- [ ] T-008: Kafka listener — consumer de eventos do worker (~2h)
- [ ] T-009: Controller `MLController` — endpoints REST (~2h)
- [ ] T-010: Validações FluentValidation para publicação (~1h)

## Ingestion (Go)

- [ ] T-011: Scaffold do worker Go (main, config, health) (~2h)
- [ ] T-012: Handler webhook de pedidos (validação + parse) (~3h)
- [ ] T-013: Handler webhook de itens (validação + parse) (~2h)
- [ ] T-014: Producer Kafka (publicar eventos) (~2h)
- [ ] T-015: Rate limiter para API do ML (~2h)
- [ ] T-016: Retry com backoff exponencial (~2h)
- [ ] T-017: Tabela `webhook_events` (idempotência) + migration (~1h)
- [ ] T-018: Tabela `ml_tokens` no banco do worker (~1h)

## Frontend (React)

- [ ] T-019: Tela de publicação ML — seleção de produtos (~3h)
- [ ] T-020: Componente `MLStatusBadge` (Published/Pending/Error) (~1h)
- [ ] T-021: Tela de status ML por produto (~2h)
- [ ] T-022: Tela de pedidos ML (listagem + detalhe) (~3h)
- [ ] T-023: Hook `useMLStatus` (react-query) (~1h)
- [ ] T-024: Hook `useMLOrders` (react-query) (~1h)
- [ ] T-025: Integração com dashboard (widget de stats ML) (~2h)

## Infra

- [ ] T-026: Docker Compose — adicionar worker Go (~1h)
- [ ] T-027: Docker Compose — adicionar Kafka + Zookeeper (~2h)
- [ ] T-028: Configuração de webhooks no ML (URL do worker) (~1h)

## Dependências

```
T-004 → T-005 (precisa de auth antes de publicar)
T-005 → T-006 (publicação antes de sync)
T-011 → T-012, T-013 (scaffold antes de handlers)
T-012 → T-014 (handler antes de producer)
T-008 → T-014 (consumer precisa de producer)
T-019 → T-005 (UI precisa do endpoint de publicação)
T-022 → T-007 (UI precisa de pedidos criados)
T-025 → T-009 (dashboard precisa de stats endpoint)
```

## Estimativa total

| Módulo | Horas |
|--------|-------|
| Backend | ~24h |
| Ingestion | ~14h |
| Frontend | ~13h |
| Infra | ~4h |
| **Total** | **~55h** |
