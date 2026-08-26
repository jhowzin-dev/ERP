---
version: 1
status: draft
---

# Tasks — Dashboard de Gestão

## Legenda

- `[ ]` pendente | `[~]` em andamento | `[x]` concluído | `[-]` cancelado

## Backend (Java/Spring)

- [ ] T-001: Query `DashboardSummaryQuery` — aggregation de KPIs (~3h)
- [ ] T-002: Query `SalesChartQuery` — vendas por dia com período (~3h)
- [ ] T-003: Query `RecentOrdersQuery` — últimos N pedidos (~2h)
- [ ] T-004: Query `DashboardAlertsQuery` — estoque baixo + pedidos pendentes + erros ML (~3h)
- [ ] T-005: Controller `DashboardController` — endpoints REST (~2h)
- [ ] T-006: Cache Redis para queries do dashboard (opt-in) (~2h)

## Frontend (React)

- [ ] T-007: `DashboardPage.tsx` — layout da página com lazy loading (~2h)
- [ ] T-008: `SummaryCards.tsx` — cards de KPI com ícones e cores (~2h)
- [ ] T-009: `SalesChart.tsx` — gráfico de linha com Recharts (~3h)
- [ ] T-010: `RecentOrders.tsx` — lista de pedidos recentes (~2h)
- [ ] T-011: `AlertsPanel.tsx` — painel de alertas (~2h)
- [ ] T-012: `MLStatusWidget.tsx` — widget de resumo ML (~1h)
- [ ] T-013: Hooks `useDashboardSummary`, `useSalesChart`, `useRecentOrders` (~2h)
- [ ] T-014: Service `dashboard-api.ts` + `dashboard-keys.ts` (~1h)
- [ ] T-015: Skeleton loading para cada componente (~1h)

## Infra

- [ ] T-016: Índices no banco para queries de agregação (~1h)
- [ ] T-016: Configuração de cache TTL no Redis (~1h)

## Dependências

```
T-001 → T-005 (query antes de controller)
T-007 → T-008, T-009, T-010, T-011 (layout antes de componentes)
T-014 → T-013 (service antes de hooks)
T-015 → T-007 (skeleton antes da página)
```

## Estimativa total

| Módulo | Horas |
|--------|-------|
| Backend | ~15h |
| Frontend | ~16h |
| Infra | ~2h |
| **Total** | **~33h** |
