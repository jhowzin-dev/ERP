---
version: 1
status: draft
---

# Spec — Integração Mercado Livre

## 1. Contrato de dados

### Product (ML Publication)

```typescript
// Frontend → Backend
interface PublishProductRequest {
  productId: number;        // ID interno do produto
  categoryId: string;       // ID da categoria no ML
  condition: "new" | "used";
  listingType: "gold_special" | "gold_pro";  // tipo de anúncio
}

// Backend → ML API
interface MLItemRequest {
  title: string;
  category_id: string;
  price: number;
  currency_id: "BRL";
  quantity: number;
  condition: "new" | "used";
  buying_mode: "buy_it_now";
  listing_type_id: string;
  description?: string;
  pictures?: { source: string }[];
  attributes?: { id: string; value_name: string }[];
}

// ML API → Backend
interface MLItemResponse {
  id: string;               // ML item_id
  status: "active" | "paused" | "closed";
  title: string;
  price: number;
  quantity: number;
  permalink: string;
}
```

### Order (Webhook)

```typescript
// Webhook payload do ML
interface MLWebhookOrder {
  resource: string;         // "/orders/12345"
  user_id: number;
  topic: "orders";
  application_id: number;
}

// Backend (após fetch do pedido)
interface InternalOrder {
  externalId: string;       // ID do ML
  buyerName: string;
  buyerEmail: string;
  items: OrderItem[];
  totalAmount: number;
  status: "NEW" | "PROCESSING" | "SHIPPED" | "DELIVERED" | "CANCELLED";
  createdAt: Date;
}

interface OrderItem {
  productId: number;        // ID interno
  mlItemId: string;         // ID no ML
  quantity: number;
  unitPrice: number;
}
```

### Stock Event

```typescript
// Kafka topic: ml.stock
interface StockChangedEvent {
  productId: number;
  previousQuantity: number;
  newQuantity: number;
  reason: "SALE" | "ADJUSTMENT" | "RETURN" | "ML_SALE";
  timestamp: Date;
}
```

## 2. Endpoints

### Backend API

| Método | Path | Body | Response | Status |
|--------|------|------|----------|--------|
| `POST` | `/api/catalog/products/{id}/publish-to-ml` | `PublishProductRequest` | `{ mlItemId: string, status: string }` | 201, 400, 409 |
| `DELETE` | `/api/catalog/products/{id}/unpublish-from-ml` | — | `{ success: boolean }` | 200, 404 |
| `GET` | `/api/catalog/products/{id}/ml-status` | — | `{ mlItemId, status, lastSync }` | 200, 404 |
| `PUT` | `/api/catalog/products/{id}/ml-price` | `{ price: number }` | `{ synced: boolean }` | 200, 400 |
| `GET` | `/api/ml/orders` | query: `status, page, limit` | `{ orders: InternalOrder[], total }` | 200 |
| `GET` | `/api/ml/stats` | — | `{ published, salesToday, lowStock }` | 200 |

### Worker Go (Webhooks)

| Método | Path | Body | Response | Status |
|--------|------|------|----------|--------|
| `POST` | `/webhooks/orders` | MLWebhookOrder | `{ received: true }` | 200, 401, 422 |
| `POST` | `/webhooks/items` | MLWebhookItem | `{ received: true }` | 200, 401, 422 |
| `GET` | `/health` | — | `{ status: "ok" }` | 200 |

## 3. Regras de validação

| Campo | Regra | Erro |
|-------|-------|------|
| `productId` | Obrigatório, existe no catálogo | `PRODUCT_NOT_FOUND` |
| `categoryId` | Obrigatório, válida no ML | `INVALID_CATEGORY` |
| `price` | > 0, <= 10.000 (ML limit) | `INVALID_PRICE` |
| `quantity` | >= 0, integer | `INVALID_QUANTITY` |
| `title` | 1-60 caracteres | `TITLE_TOO_LONG` |

## 4. Regras de negócio

- **RN-ML-01**: Um produto só pode ter 1 publicação ativa no ML por vez.
- **RN-ML-02**: Estoque não pode ficar negativo. Se ML vendeu mais que o interno, registrar conflito.
- **RN-ML-03**: Preço no ML nunca pode ser R$ 0,00.
- **RN-ML-04**: Webhook duplicado (mesmo `resource` + `user_id`) é ignorado (idempotência).
- **RN-ML-05**: Se OAuth token expirar, worker tenta refresh. Se falhar, envia alerta e para de sincronizar até resolução manual.

## 5. Testes

### Happy Path
- Publicar produto → ML retorna item_id → produto com status "Published"
- Webhook de pedido → pedido criado → estoque decrementado
- Alterar preço → ML atualizado → preço refletido em < 5 min

### Edge Cases
- Publicar produto com estoque zero → ML aceita? (verificar)
- Dois webhooks do mesmo pedido ao mesmo tempo → idempotência
- ML retorna erro 429 (rate limit) → retry com backoff
- Kafka indisponível → worker mantém webhooks em buffer local

## 6. Integrações

| Serviço | Protocolo | Autenticação | Uso |
|---------|-----------|-------------|-----|
| Mercado Livre API | REST HTTPS | OAuth 2.0 (access_token + refresh_token) | Publicação, atualização, consulta |
| Mercado Livre Webhooks | POST HTTPS | Assinatura HMAC | Notificações de pedidos/itens |
| Apache Kafka | TCP | SASL (se produção) | Eventos assíncronos |
| PostgreSQL (worker) | TCP | User/Pass | Tokens, estado de webhooks |
| Backend Java | REST interno | Nenhum (rede interna) | Consome eventos, expõe endpoints |
