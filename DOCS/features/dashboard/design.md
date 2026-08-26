---
version: 1
status: draft
---

# Design — Dashboard de Gestão

## 1. Visão técnica

O dashboard é uma página SPA no frontend que consome endpoints de aggregation
no backend. O backend calcula KPIs a partir dos dados existentes (catálogo,
estoque, pedidos, publicações ML) e retorna dados prontos para visualização.

## 2. Arquitetura

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Frontend    │────►│  Backend API │────►│  PostgreSQL  │
│  (React)     │     │  (Java)      │     │              │
│  Dashboard   │     │  Aggregation │     │  Catálogo +  │
│  Page        │     │  Queries     │     │  Pedidos     │
└──────────────┘     └──────────────┘     └──────────────┘
                            │
                            │ consome eventos
                            ▼
                     ┌──────────────┐
                     │  Kafka       │
                     │  (ML events) │
                     └──────────────┘
```

## 3. Tecnologias

| Componente | Tecnologia | Justificativa |
|-----------|-----------|---------------|
| Gráficos | Recharts | Leve, React-native, boa API |
| Polling | React Query (refetchInterval) | Cache + auto-refresh |
| Backend | Spring Boot + JPQL queries | Agregações diretas no banco |
| Cache | Redis (opcional) | KPIs não precisam de frescor absoluto |

## 4. Endpoints

| Método | Path | Response | Cache |
|--------|------|----------|-------|
| `GET` | `/api/dashboard/summary` | `{ totalProducts, totalOrdersToday, revenueToday, lowStockCount, mlPublished }` | 30s |
| `GET` | `/api/dashboard/sales-chart` | `{ data: [{date, count, revenue}] }` (7d/30d) | 60s |
| `GET` | `/api/dashboard/recent-orders` | `{ orders: [{id, buyer, total, status, date}] }` (últimos 5) | 30s |
| `GET` | `/api/dashboard/alerts` | `{ lowStock: [...], pendingOrders: [...], mlErrors: [...] }` | 60s |

## 5. Componentes Frontend

```
features/dashboard/
├── DashboardPage.tsx          ← Página principal
├── components/
│   ├── SummaryCards.tsx       ← Cards de KPI (vendas, receita, etc.)
│   ├── SalesChart.tsx        ← Gráfico de linha (Recharts)
│   ├── RecentOrders.tsx      ← Lista de pedidos recentes
│   ├── AlertsPanel.tsx       ← Painel de alertas (estoque baixo, erros ML)
│   └── MLStatusWidget.tsx    ← Widget de resumo ML
├── hooks/
│   ├── useDashboardSummary.ts
│   ├── useSalesChart.ts
│   └── useRecentOrders.ts
└── service/
    ├── dashboard-api.ts
    └── dashboard-keys.ts
```

## 6. Riscos

| Risco | Mitigação |
|-------|-----------|
| Queries de agregação lentas | Índices no banco, cache Redis, paginação |
| Dashboard carrega lento | Lazy loading, skeleton screens, dados em paralelo |
| Dados desatualizados | Polling com intervalo configurável, invalidação manual |
