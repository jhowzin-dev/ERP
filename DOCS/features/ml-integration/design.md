---
version: 1
status: draft
---

# Design — Integração Mercado Livre

## 1. Visão técnica

A integração usa um worker Go como ponte entre a API do Mercado Livre e o
backend Java. Webhooks do ML chegam no worker, que publica eventos no Kafka.
O backend consome esses eventos e atualiza o catálogo/estoque. A publicação
de produtos é feita diretamente do backend via API REST do ML.

## 2. Arquitetura

```
┌─────────────┐     ┌──────────────┐     ┌─────────┐     ┌──────────────┐
│  ML API     │◄────│  Worker Go   │────►│  Kafka  │────►│  Backend     │
│  (REST +    │     │  (webhooks + │     │         │     │  (Java/Spring│
│   Webhooks) │     │   sync)      │     │         │     │   Modulith)  │
└─────────────┘     └──────────────┘     └─────────┘     └──────────────┘
                           │                                    │
                           │                                    │
                    ┌──────────────┐                     ┌──────────────┐
                    │  PostgreSQL  │                     │  PostgreSQL  │
                    │  (worker)    │                     │  (backend)   │
                    └──────────────┘                     └──────────────┘
```

## 3. Tecnologias envolvidas

| Componente | Tecnologia | Justificativa |
|-----------|-----------|---------------|
| Worker Go | Go 1.22 + kafka-go | Performance, baixo overhead, concorrência nativa |
| Kafka | Apache Kafka | Queue robusta, replay de eventos, decoupling |
| API ML | REST + OAuth 2.0 | API oficial do Mercado Livre |
| Backend | Spring Boot + Modulith | Consumo de eventos, persistência, regras de negócio |
| Backend → ML | Feign Client ou RestTemplate | Publicação de produtos, atualização de estoque |

## 4. Fluxos principais

### 4.1 Publicação de produto

```
1. Vendedor seleciona produtos no catálogo interno
2. Frontend envia POST /api/catalog/products/{id}/publish-to-ml
3. Backend cria registro "PendingPublication"
4. Backend chama ML API: POST /items (com dados do produto)
5. ML retorna item_id
6. Backend atualiza produto com ml_item_id + status "Published"
7. Frontend recebe confirmação
```

### 4.2 Recebimento de webhook (pedido)

```
1. ML envia POST /webhooks/orders para o worker Go
2. Worker valida assinatura do webhook
3. Worker extrai dados do pedido
4. Worker publica evento "OrderReceived" no Kafka (tópico: ml.orders)
5. Backend consome evento
6. Backend cria pedido interno com status "Novo"
7. Backend atualiza estoque do produto
```

### 4.3 Sync de estoque

```
1. Estoque interno muda (venda, ajuste, devolução)
2. Backend publica evento "StockChanged" no Kafka
3. Worker consome evento
4. Worker chama ML API: PUT /items/{ml_item_id} (atualiza quantity)
5. Worker confirma sync
6. Se falha, retry com backoff exponencial (max 5 tentativas)
```

## 5. Decisões técnicas

- **Kafka como intermediário**: decoupling entre worker e backend. Se o backend cair, webhooks ficam na fila.
- **Worker separado do backend**: isolamento de responsabilidade. Worker lida com ML; backend lida com negócio.
- **Tabelas próprias no worker**: worker tem seu próprio PostgreSQL para estado de webhooks e tokens ML (não polui o banco do backend).
- **Retry com DLQ**: eventos que falharam 5x vão para Dead Letter Queue para investigação manual.

## 6. Riscos técnicos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| ML muda API sem aviso | Média | Alto | Contrato de dados flexível, testes de integração, monitoramento de erros |
| Rate limit do ML atingido | Alta | Médio | Rate limiter no worker, fila de retry, batch de publicação |
| Webhook perdido | Baixa | Alto | Idempotência, replay do Kafka, health check do worker |
| Token OAuth expira | Alta | Médio | Refresh automático, alerta quando refresh falhar |
| Kafka cai | Baixa | Alto | Kafka clusterizado, worker retenta, backend tem fallback |
