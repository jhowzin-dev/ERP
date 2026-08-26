# SG-MULTIDIA

> Sistema de gestão leve e rápido para **publicação de produtos no Mercado Livre e gestão de catálogo multi-produto**, com integração nativa ao ML.
> Monorepo com API Java (Spring Boot 4 + Modulith), worker Go (ingestão) e frontend React (Vite + Tailwind).

![Java](https://img.shields.io/badge/Java-21-ED8B00)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-4.0.7-6DB33F)
![React](https://img.shields.io/badge/React-19-61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-strict-3178C6)
![Vite](https://img.shields.io/badge/Vite-8-646CFF)
![Tailwind](https://img.shields.io/badge/Tailwind%20CSS-v4-06B6D4)
![Go](https://img.shields.io/badge/Go-1.22-00ADD8)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791)
![Kafka](https://img.shields.io/badge/Kafka-Apache-231F20)
![Arquitetura](https://img.shields.io/badge/Arquitetura-Modulith-2E8B57)

---

## Índice

1. [Visão geral](#1-visão-geral)
2. [Principais funcionalidades](#2-principais-funcionalidades)
3. [Arquitetura da solução](#3-arquitetura-da-solução)
4. [Diagrama de arquitetura](#4-diagrama-de-arquitetura)
5. [Estrutura de pastas](#5-estrutura-de-pastas)
6. [Tecnologias utilizadas](#6-tecnologias-utilizadas)
7. [Padrões arquiteturais adotados](#7-padrões-arquiteturais-adotados)
8. [Modelo de dados](#8-modelo-de-dados)
9. [Fluxo de integração ML](#9-fluxo-de-integração-ml)
10. [Fluxo de navegação](#10-fluxo-de-navegação)
11. [Fluxo de requisições HTTP](#11-fluxo-de-requisições-http)
12. [Gerenciamento de estado](#12-gerenciamento-de-estado)
13. [Estratégia de cache e eventos](#13-estratégia-de-cache-e-eventos)
14. [Tratamento de erros](#14-tratamento-de-erros)
15. [Configurando o ambiente](#15-configurando-o-ambiente)
16. [Executando o projeto](#16-executando-o-projeto)
17. [Build e CI/CD](#17-build-e-cicd)
18. [Convenções do projeto](#18-convenções-do-projeto)

---

## 1. Visão geral

### Objetivo de negócio

O SG-MULTIDIA é um ERP leve focado em **publicar e gerenciar produtos no Mercado Livre** (catálogo multi-produto, multi-segmento — ex.: multimídia, comunicação visual, impressão), com integração nativa ao ML. O MVP combina publicação automatizada de produtos, sync de estoque/preço via Kafka e um dashboard de gestão.

### Problemas que resolve

| Problema | Como o sistema resolve |
| -------- | ---------------------- |
| Publicar produtos no ML é manual, um a um | Publicação em lote via API do ML, com status de cada item |
| Estoque e preço ficam desatualizados no ML | Sync automático via worker Go + Kafka (< 5 min) |
| Pedidos do ML chegam por e-mail e precisam ser digitados | Webhooks do ML → worker → Kafka → backend cria pedido automaticamente |
| Não há visão centralizada do negócio | Dashboard com KPIs: vendas, estoque baixo, pedidos pendentes, resumo ML |
| Catálogo de produtos sem gestão | CRUD de catálogo com categorias, preços, estoque e multi-segmento |

### Personas

| Persona | O que faz |
| ------- | --------- |
| Vendedor/Lojista | Publica produtos no ML, gerencia catálogo, acompanha pedidos |
| Gestor | Vê dashboard com KPIs, toma decisões rápidas |
| Operador | Gerencia estoque, preços e integrações |

---

## 2. Principais funcionalidades

### MVP — Integração Mercado Livre
- Publicação de produtos no ML (individual e em lote)
- Sync automático de estoque (< 5 min)
- Sync automático de preço (< 5 min)
- Recebimento de pedidos via webhooks
- Dashboard de resumo ML (produtos publicados, vendas, erros)

### MVP — Dashboard
- Cards de KPI (vendas do dia, receita, estoque baixo, pedidos pendentes)
- Gráfico de vendas (7d / 30d / 90d) com comparativo
- Alertas de estoque baixo
- Lista de pedidos recentes
- Widget de resumo ML

### Catálogo de produtos
- CRUD de produtos com categorias, preços, estoque
- Multi-segmento (multimídia, comunicação visual, impressão, etc.)
- Imagens por produto
- Status de publicação ML por produto

### Gestão de estoque
- Controle de estoque por produto
- Alertas de estoque baixo
- Ajustes manuais e automáticos (via sync ML)
- Histórico de movimentações (SALE, ADJUSTMENT, ML_SALE, RETURN)

### Gestão de pedidos
- Pedidos internos e do ML em lista única
- Status do pedido (Novo, Processando, Enviado, Entregue, Cancelado)
- Detalhe do pedido com itens, valores e rastreio

---

## 3. Arquitetura da solução

O repositório é um **monorepo** com três aplicações independentes e uma pasta de documentação (`docs/`).

| Aplicação | Stack | Papel |
| --------- | ----- | ----- |
| `backend/` | Java 21 + Spring Boot 4.0.7 + Modulith (Maven) | API REST — domínio, casos de uso, persistência, integração ML |
| `ingestion/` | Go 1.22 + kafka-go | Worker — webhooks ML, sync estoque/preço, consumer Kafka |
| `frontend/` | React 19 + TypeScript 6 + Vite 8 + Tailwind v4 | SPA — catálogo, dashboard, gestão |

### Módulos do backend (Spring Modulith)

```mermaid
flowchart TB
    ROOT["com.sgmultidia.backend"]

    subgraph catalog["📦 catalog"]
        C_API["api/"]
        C_INT["internal/"]
    end

    subgraph marketplace["🛒 marketplace"]
        M_API["api/"]
        M_INT["internal/"]
    end

    subgraph inventory["📋 inventory"]
        I_API["api/"]
        I_INT["internal/"]
    end

    subgraph sales["💰 sales"]
        S_API["api/"]
        S_INT["internal/"]
    end

    subgraph finance["💹 finance"]
        F_API["api/"]
        F_INT["internal/"]
    end

    subgraph customers["👤 customers"]
        CU_API["api/"]
        CU_INT["internal/"]
    end

    subgraph production["🏭 production"]
        P_API["api/"]
        P_INT["internal/"]
    end

    subgraph events["⚡ events"]
        E_INT["internal/"]
    end

    ROOT --> catalog
    ROOT --> marketplace
    ROOT --> inventory
    ROOT --> sales
    ROOT --> finance
    ROOT --> customers
    ROOT --> production
    ROOT --> events
```

Cada módulo segue a convenção `api/` (controllers) + `internal/` (services, repositories, entities) + `package-info.java`.

### Dependências entre módulos

```mermaid
flowchart LR
    CAT["catalog<br/>📦"]
    MKT["marketplace<br/>🛒"]
    INV["inventory<br/>📋"]
    SAL["sales<br/>💰"]
    FIN["finance<br/>💹"]
    CUST["customers<br/>👤"]
    PROD["production<br/>🏭"]
    EVT["events<br/>⚡"]

    MKT --> CAT
    MKT --> INV
    SAL --> CAT
    SAL --> CUST
    SAL --> INV
    FIN --> SAL
    INV --> EVT
    MKT --> EVT
    SAL --> EVT
    PROD --> INV
```

---

## 4. Diagrama de arquitetura

### 4.1 Visão de contêineres

```mermaid
flowchart TB
    subgraph browser["Navegador"]
        FE["React 19 SPA<br/>Vite · Tailwind · react-query"]
    end

    subgraph backend["Backend Java (porta 8080)"]
        API["Spring Boot 4.0.7<br/>Spring Modulith"]
        MOD["Módulos:<br/>catalog · marketplace · inventory<br/>sales · finance · customers · production"]
        KAFKA_P["Kafka Producer"]
        KAFKA_C["Kafka Consumer"]
    end

    subgraph worker["Worker Go (porta 8081)"]
        GO["Ingestion Service<br/>kafka-go"]
        WH["Webhook Handlers"]
        SYNC["Sync Service"]
    end

    subgraph data["Dados"]
        PG[("PostgreSQL 15")]
        KFK[("Apache Kafka")]
    end

    subgraph ext["Serviços Externos"]
        ML["Mercado Livre API<br/>REST + OAuth 2.0"]
    end

    FE -->|"axios · JSON/HTTPS"| API
    API --> MOD
    MOD --> KAFKA_P
    KAFKA_C --> MOD
    KAFKA_P --> KFK
    KFK --> KAFKA_C
    KFK --> GO
    GO --> WH
    GO --> SYNC
    WH -->|"webhooks"| ML
    SYNC -->|"PUT /items"| ML
    MOD --> PG
    GO --> PG
```

### 4.2 Como cada componente se comunica

| Origem | Destino | Protocolo / mecanismo | Autenticação |
| ------ | ------- | --------------------- | ------------ |
| Frontend | Backend | HTTPS/JSON (axios) | JWT (futuro) |
| Backend | PostgreSQL | JDBC (Spring Data JPA) | Connection string |
| Backend | Kafka | TCP (Spring Kafka) | SASL (produção) |
| Worker Go | ML API | HTTPS/JSON | OAuth 2.0 |
| Worker Go | Kafka | TCP (kafka-go) | SASL (produção) |
| Worker Go | PostgreSQL | TCP (lib pg) | Connection string |
| ML API | Worker Go | HTTPS (webhooks) | Assinatura HMAC |

### 4.3 Ambiente de produção

```mermaid
flowchart TB
    subgraph users["Usuários"]
        U["Navegador"]
        ML_USERS["Mercado Livre"]
    end

    subgraph dmz["DMZ"]
        LB["Load Balancer"]
        CDN["CDN / Nginx"]
    end

    subgraph app["Aplicação"]
        FE_BE["Frontend<br/>(Nginx)"]
        BE1["Backend 1<br/>:8080"]
        BE2["Backend 2<br/>:8080"]
        ING1["Worker 1<br/>:8081"]
        ING2["Worker 2<br/>:8081"]
    end

    subgraph event["Eventos"]
        K1["Kafka Broker 1"]
        K2["Kafka Broker 2"]
        K3["Kafka Broker 3"]
    end

    subgraph storage["Armazenamento"]
        PG_M["PostgreSQL<br/>Primary"]
        PG_R["PostgreSQL<br/>Replica"]
    end

    U --> CDN --> LB
    ML_USERS --> LB
    LB --> FE_BE
    LB --> BE1
    LB --> BE2
    BE1 --> K1
    BE2 --> K2
    K1 --> K3
    ING1 --> K1
    ING2 --> K2
    BE1 --> PG_M
    BE2 --> PG_M
    PG_M --> PG_R
```

---

## 5. Estrutura de pastas

### Raiz do monorepo

```
SG-MULTIDIA/
├─ .github/workflows/      # CI/CD: build+testes, Docker build, deploy
├─ backend/                # API Java (Spring Boot + Modulith)
├─ frontend/               # SPA React (Vite + Tailwind)
├─ ingestion/              # Worker Go (Kafka + webhooks ML)
├─ docs/                   # SDD, ADRs, agents, skills, features
├─ .claude/                # Agents e skills (padrão EmpregaNet)
│   ├─ agents/             # 8 agents com frontmatter
│   └─ skills/             # 5 skills
├─ CLAUDE.md               # Contexto rápido para IA
├─ harness.ps1             # Validação Windows
└─ harness.sh              # Validação Linux/macOS
```

### `backend/`

| Caminho | Responsabilidade |
| ------- | ---------------- |
| `pom.xml` | Dependências: Spring Boot 4.0.7, Modulith 2.1.0, Flyway, Kafka, Security, Sentry 8.53, OTel |
| `Dockerfile` | Imagem multi-stage (JDK 25 → JRE) |
| `docker-compose.yml` | Postgres, Kafka, API |
| `src/main/java/.../catalog/` | Catálogo: CRUD de produtos, categorias, imagens |
| `src/main/java/.../catalog/api/` | Controllers REST do catálogo |
| `src/main/java/.../catalog/internal/` | Services, repositories, entities do catálogo |
| `src/main/java/.../marketplace/` | Integração ML: publicação, sync, webhooks |
| `src/main/java/.../inventory/` | Estoque: controle, alertas, ajustes, movimentações |
| `src/main/java/.../sales/` | Vendas: pedidos, status, rastreio |
| `src/main/java/.../finance/` | Financeiro: receitas, despesas |
| `src/main/java/.../customers/` | Clientes: cadastro, dados |
| `src/main/java/.../production/` | Produção: ordens, status |
| `src/main/java/.../events/` | Eventos cross-domain (Kafka producer/consumer) |
| `src/main/resources/` | Configurações, migrations Flyway |

### `frontend/src/`

| Caminho | Responsabilidade |
| ------- | ---------------- |
| `main.tsx` · `App.tsx` | Entry point e rotas |
| `features/products/` | CRUD de produtos |
| `features/marketplace/` | Integração ML (publicação, status) |
| `features/inventory/` | Gestão de estoque |
| `features/sales/` | Pedidos |
| `features/customers/` | Clientes |
| `features/dashboard/` | Dashboard de gestão |
| `components/layout/` | Layout, sidebar, header |
| `lib/` | Utilitários, helpers |

### `ingestion/`

| Caminho | Responsabilidade |
| ------- | ---------------- |
| `cmd/worker/main.go` | Entry point do worker |
| `internal/worker/worker.go` | Lógica principal do worker |
| `internal/worker/handlers.go` | Handlers de eventos/webhooks |
| `internal/config/config.go` | Configuração via environment |
| `Dockerfile` | Imagem multi-stage (Go builder → Alpine) |

---

## 6. Tecnologias utilizadas

### Backend

| Tecnologia | Versão | Para que serve |
| ---------- | ------ | -------------- |
| Java | 21 (JDK 21 LTS) | Runtime |
| Spring Boot | 4.0.7 | Framework web |
| Spring Modulith | 2.1.0 | Modularidade (pacotes por domínio) |
| Spring Data JPA + Hibernate | (via boot) | ORM e persistência |
| Flyway | (via boot) | Migrations do banco |
| Spring Security | (via boot) | Autenticação e autorização |
| Spring Kafka | (via boot) | Producer/Consumer de eventos |
| Spring Validation | (via boot) | Validação de beans |
| Spring Actuator | (via boot) | Health checks e métricas |
| Micrometer + OTel | (via boot) | Observabilidade e tracing |
| Sentry | 8.53.0 | Captura de erros |
| PostgreSQL | 15+ | Banco relacional |

### Frontend

| Tecnologia | Versão | Para que serve |
| ---------- | ------ | -------------- |
| React | 19.2.8 | Biblioteca de UI |
| TypeScript | 6.0.2 | Tipagem estática (strict) |
| Vite | 8.2.0 | Bundler e dev server |
| Tailwind CSS | 4.3.3 | Estilos utility-first |
| TanStack Query | 5.101.4 | Cache de dados do servidor |
| Axios | 1.19.0 | Cliente HTTP |
| React Hook Form | 7.85.0 | Formulários controlados |
| Zod | 4.4.3 | Validação de schemas |
| React Router | 7.18.2 | Roteamento SPA |
| react-i18next | 17.0.11 | Internacionalização |
| Recharts | 3.10.1 | Gráficos (dashboard) |
| oxlint | 1.75.0 | Linter (mais rápido que ESLint) |

### Ingestion (Go)

| Tecnologia | Versão | Para que serve |
| ---------- | ------ | -------------- |
| Go | 1.22 | Runtime |
| kafka-go | 0.4.47 | Consumer/Producer Kafka |
| PostgreSQL (lib) | — | Persistence de tokens e estado |

### Infraestrutura

| Tecnologia | Para que serve |
| ---------- | -------------- |
| PostgreSQL 15 | Banco relacional |
| Apache Kafka | Filas de eventos assíncronos |
| Docker + Docker Compose | Stack local |
| GitHub Actions | CI/CD |

---

## 7. Padrões arquiteturais adotados

| Padrão | Onde está | Como é aplicado |
| ------ | --------- | --------------- |
| **Modulith** | `backend/src/` | Pacotes por domínio (`catalog/`, `marketplace/`, `inventory/`, etc.) com comunicação via eventos |
| **CQRS (leve)** | Módulos | Commands mutam; queries leem. Separação por pacote `api/` vs `internal/` |
| **Repository + Service** | `internal/` por módulo | Repositórios para acesso a dados, Services para lógica de negócio |
| **Event-driven** | `events/` + Kafka | Eventos cross-domain via Kafka (ex.: estoque mudou, produto publicado) |
| **Soft delete** | Entidades | `isDeleted` + `deletedAt` em vez de DELETE físico |
| **Feature-based (frontend)** | `frontend/src/features` | Cada feature tem seus componentes, hooks e services |
| **Atomic Design (frontend)** | `components/` | Átomos → Moléculas → Organismos |
| **Spec-Driven Development** | `docs/sdd/` | PRD → design → spec/tasks antes do código |
| **ADR** | `docs/sdd/adrs/` | Decisões estruturais documentadas |

---

## 8. Modelo de dados

### Fluxo de dados

```mermaid
flowchart TB
    subgraph entrada["Entrada de Dados"]
        FE_REQ["Frontend → API"]
        ML_WH["Webhooks ML"]
        ML_SYNC["Sync estoque/preço"]
    end

    subgraph backend["Backend (Modulith)"]
        CAT["catalog<br/>Produtos · Categorias"]
        MKT["marketplace<br/>Publicações ML"]
        INV["inventory<br/>Estoque"]
        SAL["sales<br/>Pedidos"]
        FIN["finance<br/>Financeiro"]
        CUST["customers<br/>Clientes"]
    end

    subgraph eventos["Eventos (Kafka)"]
        E1["ProductPublished"]
        E2["StockChanged"]
        E3["OrderReceived"]
        E4["PriceSynced"]
    end

    subgraph persist["Persistência"]
        PG[("PostgreSQL")]
    end

    FE_REQ --> CAT
    FE_REQ --> SAL
    FE_REQ --> INV
    ML_WH --> MKT
    ML_SYNC --> INV

    CAT --> E1
    INV --> E2
    MKT --> E3
    INV --> E4

    CAT --> PG
    MKT --> PG
    INV --> PG
    SAL --> PG
    FIN --> PG
    CUST --> PG
```

### Agregados principais

```mermaid
erDiagram
  PRODUCTS ||--o{ PRODUCT_IMAGES : "possui"
  PRODUCTS }o--|| CATEGORIES : "pertence"
  PRODUCTS ||--o{ PRODUCT_PUBLICATIONS : "publicado como"
  PRODUCTS ||--o{ STOCK_MOVEMENTS : "movimentações"
  PRODUCT_PUBLICATIONS }o--|| MARKETPLACES : "no marketplace"
  ORDERS ||--o{ ORDER_ITEMS : "contém"
  ORDER_ITEMS }o--|| PRODUCTS : "produto"
  ORDERS }o--o| CUSTOMERS : "cliente de"

  PRODUCTS {
    bigint id PK
    string name
    string description
    decimal price
    int stock_quantity
    bigint category_id FK
    bool is_deleted
    timestamptz created_at
    timestamptz updated_at
  }

  CATEGORIES {
    bigint id PK
    string name
    string segment
    bool is_deleted
  }

  PRODUCT_PUBLICATIONS {
    bigint id PK
    bigint product_id FK
    string marketplace_item_id
    string marketplace "ML | MAGALU | AMAZON"
    string status "PUBLISHED | PENDING | ERROR"
    timestamptz last_sync
    timestamptz created_at
  }

  STOCK_MOVEMENTS {
    bigint id PK
    bigint product_id FK
    int previous_quantity
    int new_quantity
    string reason "SALE | ADJUSTMENT | ML_SALE | RETURN"
    timestamptz created_at
  }

  ORDERS {
    bigint id PK
    string external_id "ID do marketplace"
    bigint customer_id FK
    decimal total_amount
    string status "NEW | PROCESSING | SHIPPED | DELIVERED | CANCELLED"
    string source "INTERNAL | ML"
    timestamptz created_at
  }

  ORDER_ITEMS {
    bigint id PK
    bigint order_id FK
    bigint product_id FK
    int quantity
    decimal unit_price
  }

  CUSTOMERS {
    bigint id PK
    string name
    string email
    string phone
    string cpf_cnpj
    bool is_deleted
    timestamptz created_at
  }
```

### Ciclo de vida do produto (publicação ML)

```mermaid
stateDiagram-v2
    [*] --> DRAFT : Criação
    DRAFT --> PUBLISHED : POST /publish-to-ml
    PUBLISHED --> SYNCING : Evento StockChanged
    SYNCING --> PUBLISHED : Sync OK
    SYNCING --> ERROR : Sync falhou (max 5 retries)
    ERROR --> SYNCING : Retry
    PUBLISHED --> UNPUBLISHED : DELETE /unpublish
    UNPUBLISHED --> [*]

    note right of PUBLISHED
        Produto visível no ML
        ml_item_id preenchido
    end note

    note right of SYNCING
        Worker Go consome Kafka
        PUT /items/{ml_item_id}
    end note
```

---

## 9. Fluxo de integração ML

### 9.1 Publicação de produto no ML

```mermaid
sequenceDiagram
    autonumber
    participant V as Vendedor
    participant FE as Frontend
    participant BE as Backend Java
    participant ML as Mercado Livre API
    participant K as Kafka

    V->>FE: Seleciona produtos
    FE->>BE: POST /api/catalog/products/{id}/publish-to-ml
    BE->>BE: Cria "PendingPublication"
    BE->>ML: POST /items
    ML-->>BE: item_id
    BE->>BE: Atualiza produto (ml_item_id + Published)
    BE->>K: Evento ProductPublished
    BE-->>FE: Confirmação
```

### 9.2 Recebimento de webhook (pedido ML)

```mermaid
sequenceDiagram
    autonumber
    participant ML as Mercado Livre
    participant W as Worker Go
    participant K as Kafka
    participant BE as Backend Java
    participant DB as PostgreSQL

    ML->>W: POST /webhooks/orders
    W->>W: Valida assinatura HMAC
    W->>K: Evento OrderReceived
    K->>BE: Consumer
    BE->>BE: Cria pedido (status Novo)
    BE->>DB: INSERT order + UPDATE stock
```

### 9.3 Sync de estoque

```mermaid
sequenceDiagram
    autonumber
    participant BE as Backend Java
    participant K as Kafka
    participant W as Worker Go
    participant ML as Mercado Livre API

    BE->>BE: Estoque muda (venda/ajuste/devolução)
    BE->>K: Evento StockChanged
    K->>W: Consumer
    W->>ML: PUT /items/{ml_item_id}
    alt Sucesso
        W->>W: Confirma sync
    else Falha (até 5x)
        W->>W: Retry com backoff exponencial
        W->>ML: PUT /items/{ml_item_id}
    end
```

### 9.4 Fluxo de dados completo

```mermaid
flowchart LR
    subgraph entrada["Entrada"]
        U["Usuário"]
        MLWH["Webhooks ML"]
    end

    subgraph processamento["Processamento"]
        FE["Frontend React"]
        BE["Backend Java"]
        W["Worker Go"]
    end

    subgraph dados["Dados"]
        PG[("PostgreSQL")]
        KFK[("Kafka")]
    end

    subgraph saida["Saída"]
        ML["ML API"]
    end

    U --> FE --> BE --> PG
    MLWH --> W --> KFK --> BE
    BE --> ML
    W --> ML
```

---

## 10. Fluxo de navegação

```mermaid
flowchart TD
    ROOT["/"] -->|redirect| DASH["/dashboard"]

    subgraph PUB["Público — catálogo de produtos"]
        CAT_L["/catalog<br/>listagem de produtos"]
        CAT_D["/catalog/:id<br/>detalhe do produto"]
    end

    subgraph AUTHSEG["Autenticação — anônimo"]
        LOGIN["/login"]
        REGISTER["/register"]
    end

    subgraph MAIN["Área autenticada — AppShell"]
        DASH
        PROD["/products<br/>CRUD de produtos"]
        INV["/inventory<br/>gestão de estoque"]
        SAL["/sales<br/>pedidos"]
        MKT["/marketplace<br/>integração ML"]
        CUST["/customers<br/>clientes"]
        CATA["/catalog/manage<br/>gerenciar catálogo"]
        PERFIL["/account/profile"]
    end

    NAOAUT["/unauthorized"]

    CAT_L --> CAT_D
    CAT_D -->|"candidatar-se sem sessão"| LOGIN
    LOGIN -->|"sucesso"| DASH
    REGISTER --> LOGIN
    MAIN -->|"sessão ausente/expirada"| LOGIN
    MAIN -->|"role insuficiente"| NAOAUT
    PROD --> CATA
    INV --> MKT
```

---

## 11. Fluxo de requisições HTTP

### 11.1 Mutação autenticada (publicação de produto)

```mermaid
sequenceDiagram
    autonumber
    participant U as Usuário
    participant F as React Hook Form + Zod
    participant Q as TanStack Query (useMutation)
    participant AX as axios
    participant P as Spring Boot Pipeline
    participant C as CatalogController
    participant S as MarketplaceService
    participant DB as PostgreSQL
    participant K as Kafka

    U->>F: submit do formulário
    F->>F: Zod schema.parse (validação)
    F->>Q: mutateAsync(values)
    Q->>AX: POST /api/catalog/products/{id}/publish-to-ml
    AX->>P: JWT no header

    P->>P: Spring Security (Authentication)
    P->>P: Validation (@Valid)
    P->>C: publishToMl(id)
    C->>S: publishProduct(product)
    S->>S: Chama ML API: POST /items
    S->>DB: Atualiza produto (ml_item_id, status)
    S->>K: Evento ProductPublished
    S-->>C: PublicationResult
    C-->>AX: 200 OK
    AX-->>Q: sucesso
    Q->>Q: invalidateQueries(productsKeys.all())
    Q->>U: Toast de sucesso
```

### 11.2 Leitura pública (catálogo de produtos)

```mermaid
sequenceDiagram
    autonumber
    participant U as Navegador
    participant RSC as Server Component
    participant API as GET /api/catalog/products
    participant DB as PostgreSQL

    U->>RSC: GET /catalog
    RSC->>API: fetch products
    API->>DB: SELECT (is_deleted=false)
    DB-->>API: products[]
    API-->>RSC: 200 JSON
    RSC-->>U: HTML renderizado
```

---

## 12. Gerenciamento de estado

### Árvore de providers

```mermaid
flowchart TB
    A["RootLayout<br/>html lang=pt-BR"] --> B["AppProviders"]
    B --> C["QueryProvider<br/>QueryClient por montagem"]
    C --> D["AuthProvider<br/>Context API (localStorage)"]
    D --> E["ThemeProvider (tailwind)"]
    E --> F["ToasterProvider"]
    F --> G["children"]
    G --> H["Layout do grupo de rota"]
    H --> I["AppShell → Sidebar → Header"]
    I --> J["Página → componente da feature"]
```

### Hierarquia de estado

| Camada | Onde vive | Responsabilidade |
| ------ | --------- | ---------------- |
| **Server State** | TanStack Query | Cache de dados da API, mutations, invalidação |
| **Global State** | Context API | Auth, tema, config global |
| **Form State** | React Hook Form + Zod | Formulários controlados com validação |
| **Navigation State** | react-router-dom | Rota atual, parâmetros |
| **Local State** | useState / useReducer | UI local de componentes |

---

## 13. Estratégia de cache e eventos

### Camadas de cache

```mermaid
flowchart LR
    BROWSER["1. TanStack Query<br/>memória do navegador<br/>staleTime 60 s"]
    API_CACHE["2. Spring Cache<br/>(opcional, Redis futuro)"]
    DB[("3. PostgreSQL")]

    BROWSER --> API_CACHE
    API_CACHE --> DB
```

### Fluxo de eventos (Kafka)

```mermaid
flowchart TB
    subgraph producers["Producers"]
        BE["Backend Java<br/>(catalog, inventory, sales)"]
    end

    subgraph kafka["Apache Kafka"]
        TOPIC1["product.published"]
        TOPIC2["stock.changed"]
        TOPIC3["order.received"]
        TOPIC4["price.synced"]
    end

    subgraph consumers["Consumers"]
        W["Worker Go<br/>(ingestion)"]
        BE_C["Backend Java<br/>(events module)"]
    end

    BE --> TOPIC1
    BE --> TOPIC2
    BE --> TOPIC3
    BE --> TOPIC4

    TOPIC1 --> W
    TOPIC2 --> W
    TOPIC3 --> BE_C
    TOPIC4 --> W

    W -->|"PUT /items"| ML["ML API"]
    BE_C -->|"Cria pedido"| DB[("PostgreSQL")]
```

---

## 14. Tratamento de erros

### Contrato de erro — formato padronizado

Todas as respostas de erro da API têm a mesma forma:

```json
{
  "statusCode": 400,
  "code": "VALIDATION_ERROR",
  "message": "Dados inválidos",
  "details": ["Nome é obrigatório", "Preço deve ser > 0"]
}
```

### Tratamento no frontend

```mermaid
flowchart TB
    ERR["Erro em uma chamada axios"] --> IS401{"status 401?"}
    IS401 -->|Sim| REFRESH["tryRefreshSession()"]
    REFRESH -->|OK| RETRY["repete a requisição uma vez"]
    REFRESH -->|Falhou| LOGOUT["onLogout() → limpa metadados"]
    IS401 -->|Não| PARSE["parseApiError(err)"]
    PARSE --> MSG["formatDomainErrorMessage"]
    MSG --> MUT{"Origem"}
    MUT -->|Mutation| REPORT["reportMutationApiError<br/>toast + Alert"]
    MUT -->|Query| BOUND["ApiQueryBoundary<br/>ErrorFallback"]
    ERR --> RENDER{"Erro de renderização?"}
    RENDER -->|Sim| BOUNDARY["ErrorBoundary"]
    RENDER -->|Não| NF["not-found.tsx"]
```

---

## 15. Configurando o ambiente

### Pré-requisitos

| Ferramenta | Versão | Necessário para |
| ---------- | ------ | --------------- |
| JDK | 21+ | Backend |
| Node.js | 20+ | Frontend |
| Go | 1.22+ | Ingestion |
| Docker + Docker Compose | recente | Stack local |
| Maven | (wrapper incluso) | Backend build |

### Passo a passo

**1. Clonar**

```bash
git clone <url-do-repositorio> && cd SG-MULTIDIA
```

**2. Subir infraestrutura**

```bash
docker compose up -d postgres kafka
```

**3. Backend**

```bash
cd backend
.\mvnw.cmd spring-boot:run   # Windows
./mvnw spring-boot:run       # Linux/macOS
```

**4. Frontend**

```bash
cd frontend
npm install
npm run dev
```

**5. Ingestion (opcional)**

```bash
cd ingestion
go run ./cmd/worker
```

### Portas

| Serviço | Porta |
| ------- | ----- |
| Frontend (Vite) | 5173 |
| Backend (API) | 8080 |
| PostgreSQL | 5432 |
| Kafka | 9092 |
| Worker Go | 8081 |

### Variáveis de ambiente

**Backend** (`application.properties` ou env vars):

| Variável | Default | Descrição |
|----------|---------|-----------|
| `spring.datasource.url` | `jdbc:postgresql://localhost:5432/sgmultidia` | URL do banco |
| `spring.datasource.username` | `sgmultidia` | Usuário do banco |
| `spring.datasource.password` | `sgmultidia` | Senha do banco |
| `spring.kafka.bootstrap-servers` | `localhost:9092` | Kafka brokers |
| `SENTRY_DSN` | (vazio) | DSN do Sentry |
| `SENTRY_ENV` | `dev` | Ambiente |

**Ingestion** (env vars):

| Variável | Descrição |
|----------|-----------|
| `KAFKA_BROKERS` | Endereço do Kafka |
| `ML_WEBHOOK_SECRET` | Secret para validação de webhooks |
| `ML_ACCESS_TOKEN` | Token de acesso à API do ML |
| `DATABASE_URL` | Connection string do PostgreSQL |

---

## 16. Executando o projeto

### Opção A — Docker Compose (tudo junto)

```bash
docker compose up --build
```

### Opção B — Desenvolvimento local (recomendado)

Terminal 1 — Infra:
```bash
docker compose up -d postgres kafka
```

Terminal 2 — Backend:
```bash
cd backend && ./mvnw spring-boot:run
```

Terminal 3 — Frontend:
```bash
cd frontend && npm run dev
```

Terminal 4 — Ingestion:
```bash
cd ingestion && go run ./cmd/worker
```

Acesse: `http://localhost:5173`

---

## 17. Build e CI/CD

### Pipeline de build

```mermaid
flowchart LR
    PUSH["push em main<br/>ou workflow_dispatch"] --> CI

    subgraph CI["build-and-test.yml"]
        C1["setup-java 25"] --> C2["mvn clean verify"]
    end

    CI --> DOCKER

    subgraph DOCKER["docker-build.yml"]
        D1["docker build<br/>backend/Dockerfile"] --> D2["docker push<br/>GitHub Container Registry"]
    end

    DOCKER --> DEPLOY

    subgraph DEPLOY["deploy.yml"]
        E1["SSH / SSM"] --> E2["docker pull"] --> E3["docker stop/rm"] --> E4["docker run -d"]
    end
```

### Harness de validação

```bash
.\harness.ps1                # Windows (todos)
.\harness.ps1 backend        # Só backend
.\harness.ps1 frontend       # Só frontend
.\harness.ps1 ingestion      # Só ingestion
```

### Build local

Backend:
```bash
cd backend && ./mvnw clean package -DskipTests
```

Frontend:
```bash
cd frontend && npm run build
```

Ingestion:
```bash
cd ingestion && go build -o worker ./cmd/worker
```

---

## 18. Convenções do projeto

### Gerais

| Tema | Convenção |
| ---- | --------- |
| Idioma | Documentação em **pt-BR**; código em **inglês** |
| Commits | Conventional Commits: `feat:`, `fix:`, `refactor:`, `docs:`, `perf:` |
| Branch principal | `main` |
| Segredos | **Nunca** no repo. Usar env vars ou Docker Compose `.env` |

### Backend (Java/Spring)

| Tema | Convenção |
| ---- | --------- |
| Modularidade | Pacotes por domínio: `catalog/`, `marketplace/`, `inventory/`, etc. |
| Estrutura do módulo | `<modulo>/api/` (controllers) + `<modulo>/internal/` (services, repos, entities) |
| Nomenclatura | `PascalCase` para classes; `_camelCase` para campos privados |
| Sufixos | `*Controller`, `*Service`, `*Repository`, `*Entity`, `*Exception` |
| Migrations | Flyway, em `src/main/resources/db/migration/` |
| Validação | Bean Validation (annotations) + `@Valid` nos controllers |
| Eventos | Kafka via Spring Kafka; producer e consumer por módulo |
| Transações | `@Transactional` em services; eventos publicados após commit |

### Frontend (React/TypeScript)

| Tema | Convenção |
| ---- | --------- |
| Arquivos | `kebab-case` para módulos; `PascalCase` para componentes |
| Pastas | `kebab-case`; features em `src/features/` |
| Componentes | Um por arquivo, exportado nomeado |
| Tipos | `strict: true`, **`any` proibido** |
| Estilos | Tailwind CSS (utility-first) |
| Forms | React Hook Form + Zod |
| State do servidor | TanStack Query (react-query) |
| Linter | oxlint |

### Ingestion (Go)

| Tema | Convenção |
| ---- | --------- |
| Estrutura | `cmd/worker/` (entry point) + `internal/worker/` (lógica) + `internal/config/` |
| Handlers | Um handler por tipo de evento/webhook |
| Erros | Tratamento com retry + backoff exponencial |
| Config | Via environment variables |

---

## Docs

| Documento | Caminho | Quando usar |
| --------- | ------- |-------------|
| Guia de agents | `CLAUDE.md` | Contexto rápido para IA |
| Workflow dos agents | `docs/agents/README.md` | Pipeline de execução |
| SDD Orchestrator | `docs/sdd/SDD-ORCHESTRATOR.md` | Nova feature (PRD → spec) |
| ADRs | `docs/sdd/adrs/README.md` | Decisões arquiteturais |
| Feature ML | `docs/features/ml-integration/` | Integração Mercado Livre |
| Feature Dashboard | `docs/features/dashboard/` | Dashboard de gestão |
| Skills | `docs/skills/README.md` | Conhecimento especializado |
