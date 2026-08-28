---
name: go-skill
description: Convenções canónicas do serviço de ingestão Go do OminiCore — kafka-go, handlers, producers, consumers, banco de dados (PostgreSQL), testes, retry/backoff, tratamento de erros. Use ao ler, escrever ou revisar qualquer coisa em ingestion/. Não use para trabalho de UI (frontend-skill), backend Java/Spring (backend-skill) nem para especificação de feature antes de código (sdd-orchestrator).
---

# Ingestion (Go — OminiCore Worker)

Base de **conhecimento** do serviço de ingestão: fatos do repositório, padrões Go, kafka-go, banco de dados, testes e anti-padrões.
Não é um perfil de comportamento — o comportamento está no agent `go-implementer`,
que carrega esta skill como contexto obrigatório.

---

## 1. Quando aplicar

| Situação | Aplicar |
| -------- | ------- |
| Alterações em `ingestion/` (cmd, internal) | Sim |
| Novos handlers, producers, consumers Kafka | Sim |
| Repositories e migrations de banco de dados | Sim |
| Testes em `ingestion/` (Unit ou Integration) | Sim |
| Conexão com ML API (webhooks, OAuth) | Sim |
| UI, hooks, estilos | Não — [`frontend-skill`](../frontend-skill/SKILL.md) |
| Backend Java/Spring | Não — [`backend-skill`](../backend-skill/SKILL.md) |
| Especificar feature antes de código | Não — [`sdd-orchestrator`](../sdd-orchestrator/SKILL.md) |

---

## 2. Ligações

| Recurso | Path |
| ------- | ---- |
| Mapa do monorepo e comandos de build | [`docs/README.md`](../../../docs/README.md) |
| ADR Go para ingestion | [`docs/sdd/adrs/ADR-0003-ingestion-go.md`](../../../docs/sdd/adrs/ADR-0003-ingestion-go.md) |
| ADR ML integration | [`docs/sdd/adrs/ADR-0004-ml-integration.md`](../../../docs/sdd/adrs/ADR-0004-ml-integration.md) |
| Spec da feature ML | [`docs/features/ml-integration/spec.md`](../../../docs/features/ml-integration/spec.md) |
| Design da feature ML | [`docs/features/ml-integration/design.md`](../../../docs/features/ml-integration/design.md) |
| Código Go concreto | [`go-implementer`](../../agents/go-implementer.md) |
| Governo SDD (fases e gate) | [`docs/sdd/SDD-ORCHESTRATOR.md`](../../../docs/sdd/SDD-ORCHESTRATOR.md) |
| ADRs transversais | [`docs/sdd/adrs/`](../../../docs/sdd/adrs/) |

Para features com pasta de spec activa (`docs/features/<id>/`): respeitar `prd.md` / `design.md`
antes de divergir; registar desvios pragmáticos nas *deviation notes* do `tasks.md`.

---

## 3. Princípios

| Princípio | Como se traduz aqui |
| --------- | ------------------- |
| **Simplicidade** | Go favorece código simples e explícito; não adicionar abstrações "para o futuro". |
| **Tratamento de erros** | Erros são valores; sempre tratar ou propagar com contexto. |
| **Idempotência** | Handlers devem ser idempotentes para reprocessamento seguro. |
| **Testabilidade** | Interfaces para dependências externas; mocks em testes unitários. |
| **Observabilidade** | Logs estruturados, métricas, traces para diagnóstico. |

---

## 4. Estrutura de Pastas (`ingestion/`)

```
ingestion/
├── cmd/
│   └── worker/
│       └── main.go              # Entry point, configuração, DI
├── internal/
│   ├── config/
│   │   └── config.go            # Configuração via variáveis de ambiente
│   ├── worker/
│   │   ├── worker.go            # Loop principal do worker
│   │   └── handlers.go          # Handlers de webhooks Kafka
│   ├── kafka/
│   │   ├── producer.go          # Kafka producer
│   │   └── consumer.go          # Kafka consumer
│   ├── db/
│   │   ├── repository.go        # Repositories (PostgreSQL)
│   │   └── migrations.go        # Migrations
│   ├── ml/
│   │   ├── client.go            # Cliente HTTP para ML API
│   │   └── auth.go              # OAuth token management
│   └── retry/
│       └── backoff.go           # Retry com exponential backoff
├── go.mod
├── go.sum
└── Dockerfile
```

**Regra:** `cmd/` para entry points; `internal/` para lógica que não pode ser importada externamente.

---

## 5. Convenções de Código

- **Naming:** pacotes em lowercase, camelCase para variáveis/funções, PascalCase para tipos exportados.
- **Tratamento de erros:** sempre checar `err != nil`; usar `fmt.Errorf("contexto: %w", err)` para wrapping.
- **Logging:** usar `log/slog` (Go 1.21+) com níveis apropriados (Info, Warn, Error).
- **Contexto:** passar `context.Context` como primeiro parâmetro em funções que fazem I/O.
- **Variáveis de ambiente:** usar `os.Getenv` com defaults seguros; nunca hardcodar strings de conexão.
- **Graceful shutdown:** capturar sinais (SIGINT, SIGTERM) e encerrar limposmente.

---

## 6. Kafka (kafka-go)

### Producer

```go
// Exemplo de producer
writer := &kafka.Writer{
    Addr:     kafka.TCP("localhost:9092"),
    Topic:    "worker-events",
    Balancer: &kafka.LeastBytes{},
    BatchTimeout: 10 * time.Millisecond,
}
```

- Usar `kafka.Writer` para produzir mensagens.
- Configurar `BatchTimeout` para agrupar mensagens.
- Tratar erros de produção com retry.
- Fechar writer no shutdown.

### Consumer

```go
// Exemplo de consumer
reader := kafka.NewReader(kafka.ReaderConfig{
    Brokers:  []string{"localhost:9092"},
    GroupID:  "worker-group",
    Topic:    "ml-webhooks",
    MinBytes: 1,
    MaxBytes: 10e6,
})
```

- Usar `kafka.Reader` com `GroupID` para consumo balanceado.
- Configurar `MinBytes` e `MaxBytes` para eficiência.
- Marcar mensagens como processadas após sucesso.
- Tratar erros de consumo com logging e retry.

### Timeouts

- Configurar `ReadTimeout` e `WriteTimeout` no reader/writer.
- Usar `context.WithTimeout` para operações com deadline.
- Implementar circuit breaker para falhas persistentes.

---

## 7. Banco de Dados (PostgreSQL)

### Conexão

```go
// Exemplo de conexão
db, err := sql.Open("postgres", os.Getenv("DATABASE_URL"))
if err != nil {
    log.Fatal("Erro ao conectar ao banco:", err)
}
db.SetMaxOpenConns(25)
db.SetMaxIdleConns(5)
db.SetConnMaxLifetime(5 * time.Minute)
```

- Usar `database/sql` com driver `pgx` ou `pq`.
- Configurar pool de conexões adequadamente.
- Usar variável de ambiente `DATABASE_URL`.

### Repositories

- Funções que fazem query devem receber `context.Context`.
- Usar prepared statements para queries frequentes.
- Tratar erros específicos (ErrNoRows, constraints).
- Implementar soft delete quando aplicável.

### Migrations

- Usar ferramenta de migrations (ex: `golang-migrate/migrate`).
- Migrations em `internal/db/migrations/`.
- Naming: `000001_create_events_table.up.sql`.
- Forward-only: não fazer drop sem migração de dados.

---

## 8. Testes

### Stack

| Componente | Uso |
| ---------- | --- |
| `testing` | Framework padrão Go |
| `testify` | Asserts e mocks |
| `sqlmock` | Mock de banco de dados |
| `kafka-go/mock` | Mock de Kafka |
| `httptest` | Mock de servidor HTTP |

### Unit

- Um test por cenário; nome descritivo em inglês.
- Usar mocks para dependências externas (Kafka, DB, HTTP).
- Testar tanto sucesso quanto falhas.
- Prefixo: `TestNomeDoFuncao`.

### Integration

- Usar Docker Compose para serviços reais (Kafka, PostgreSQL).
- Configurar variáveis de ambiente para testes.
- Limpar dados entre testes.
- Prefixo: `TestIntegration_*`.

### Comandos

```bash
go test ./...                     # Todos os testes
go test -v ./...                  # Verbose
go test -cover ./...              # Cobertura
go test -run TestNomeFuncao ./... # Teste específico
```

---

## 9. Retry e Backoff

### Exponential Backoff

```go
// Exemplo de backoff exponencial
func Backoff(attempt int, maxDelay time.Duration) time.Duration {
    delay := time.Duration(1<<uint(attempt)) * time.Second
    if delay > maxDelay {
        delay = maxDelay
    }
    return delay
}
```

- Backoff exponencial com jitter para evitar thundering herd.
- Limite máximo de tentativas (ex: 5).
- DLQ (Dead Letter Queue) para mensagens que falharam após todas as tentativas.

### Circuit Breaker

- Abrir circuito após N falhas consecutivas.
- Fechar circuito após sucesso.
- Half-open para testar recuperação.

---

## 10. Validação (comandos reais)

```bash
go build ./...                    # Compilação
go test ./...                     # Testes
go vet ./...                      # Análise estática
go test -cover ./...              # Cobertura
.\harness.ps1 ingestion           # Harness completo
```

---

## 11. Checklist de entrega (Ingestion)

1. [ ] Handler seguindo o padrão existente (cmd/ + internal/).
2. [ ] Tratamento de erros com contexto (`fmt.Errorf` com `%w`).
3. [ ] Logging estruturado com `log/slog`.
4. [ ] Timeouts configurados em operações I/O.
5. [ ] Retry com backoff exponencial onde aplicável.
6. [ ] Testes unitários com mocks; Integração quando tocar Kafka/DB real.
7. [ ] `go build`, `go test`, `go vet` verdes.
8. [ ] Variáveis de ambiente documentadas.
9. [ ] Graceful shutdown implementado.

---

## 12. Anti-padrões

| Evitar | Porquê |
| ------ | ------ |
| Ignorar erros (`_ = err`) | Erros silenciosos causam bugs difíceis de diagnosticar |
| `panic` em código de produção | Destrói o processo; usar erros retornados |
| Hardcodar strings de conexão | Dificulta deploy e manutenção |
| Context sem deadline | Pode causar goroutines presas |
| Logger sem contexto | Dificulta diagnóstico em produção |
| Testes sem mocks | Testes frágeis e lentos |
| DLQ sem monitoramento | Mensagens perdidas sem visibilidade |
| Retry sem limite | Pode causar sobrecarga no sistema |

---

## 13. Idioma

Mensagens de utilizador e logs de negócio: **português (Brasil)**. Identificadores de código: **inglês**.

---

## Histórico

| Versão | Mudança |
| ------ | ------- |
| 1.0.0 | Versão inicial — convenções Go, kafka-go, banco de dados, testes |
