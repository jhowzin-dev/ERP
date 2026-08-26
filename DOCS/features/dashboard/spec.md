---
version: 1
status: draft
---

# Spec — Dashboard de Gestão

## 1. Contrato de dados

### Summary

```typescript
interface DashboardSummary {
  totalProducts: number;        // total de produtos no catálogo
  activeProducts: number;       // produtos ativos (não excluídos)
  totalOrdersToday: number;     // pedidos criados hoje
  revenueToday: number;         // receita do dia (R$)
  lowStockCount: number;        // produtos com estoque < mínimo
  mlPublished: number;          // produtos publicados no ML
  pendingShipments: number;     // pedidos aguardando envio
}
```

### Sales Chart

```typescript
interface SalesChartData {
  data: SalesDataPoint[];
  comparison: {
    currentPeriod: number;
    previousPeriod: number;
    changePercent: number;
  };
}

interface SalesDataPoint {
  date: string;       // YYYY-MM-DD
  count: number;      // quantidade de vendas
  revenue: number;    // receita em R$
}
```

### Recent Orders

```typescript
interface RecentOrder {
  id: number;
  buyerName: string;
  total: number;
  status: "NEW" | "PROCESSING" | "SHIPPED" | "DELIVERED" | "CANCELLED";
  source: "INTERNAL" | "ML";
  createdAt: string;  // ISO 8601
}
```

### Alerts

```typescript
interface DashboardAlerts {
  lowStock: LowStockItem[];
  pendingOrders: PendingOrder[];
  mlErrors: MLError[];
}

interface LowStockItem {
  productId: number;
  productName: string;
  currentStock: number;
  minimumStock: number;
}

interface PendingOrder {
  orderId: number;
  buyerName: string;
  daysPending: number;
}

interface MLError {
  productId: number;
  productName: string;
  errorType: string;
  lastAttempt: string;
}
```

## 2. Endpoints

| Método | Path | Query Params | Response | Status |
|--------|------|-------------|----------|--------|
| `GET` | `/api/dashboard/summary` | — | `DashboardSummary` | 200 |
| `GET` | `/api/dashboard/sales-chart` | `period: 7d \| 30d \| 90d` | `SalesChartData` | 200 |
| `GET` | `/api/dashboard/recent-orders` | `limit: number (default 5)` | `{ orders: RecentOrder[] }` | 200 |
| `GET` | `/api/dashboard/alerts` | — | `DashboardAlerts` | 200 |

## 3. Regras de validação

| Parâmetro | Regra | Erro |
|-----------|-------|------|
| `period` | Valores aceitos: `7d`, `30d`, `90d` | `INVALID_PERIOD` |
| `limit` | 1-50, default 5 | `INVALID_LIMIT` |

## 4. Regras de negócio

- **RN-DASH-01**: Dados do dashboard refletem apenas itens não excluídos (`isDeleted = false`).
- **RN-DASH-02**: "Receita do dia" soma pedidos com status `NEW`, `PROCESSING`, `SHIPPED` (exclui `CANCELLED`).
- **RN-DASH-03**: "Estoque baixo" = produtos com `currentStock < minimumStock` (campo a ser definido no catálogo).
- **RN-DASH-04**: Comparativo no gráfico usa período imediatamente anterior (7d → compara com 7 dias anteriores).

## 5. Testes

### Happy Path
- GET /api/dashboard/summary → retorna todos os campos numéricos
- GET /api/dashboard/sales-chart?period=7d → retorna 7 data points
- GET /api/dashboard/recent-orders?limit=5 → retorna até 5 pedidos

### Edge Cases
- Sem pedidos hoje → `totalOrdersToday: 0`, `revenueToday: 0`
- Sem produtos com estoque baixo → `lowStockCount: 0`, `lowStock: []`
- Banco vazio → todos os campos zerados, sem erro

## 6. Integrações

| Fonte | Dados | Via |
|-------|-------|-----|
| Catálogo (produtos) | Total, ativos, estoque | JPQL direto |
| Pedidos internos | Vendas, receita | JPQL direto |
| ML (publicações) | Produtos publicados | Tabela `ml_publications` |
| ML (erros) | Erros de sync | Tabela `ml_sync_errors` |
