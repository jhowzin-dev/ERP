# ADR 0003: Ingestão — Go com Kafka

**Status**: aceito
**Data**: 2026-08-01
**Decidido por**: Tech Lead

## Contexto

A integração com Mercado Livre gera alto volume de webhooks e necessita
de processamento assíncrono de eventos (estoque, preço, pedidos). Precisamos
de performance e baixo overhead de memória.

## Decisão

- **Go 1.22** para o worker de ingestão
- **kafka-go** como lib Kafka (síncrona, simples)
- **Consumer group** para rebalanceamento automático
- **Handlers por evento** em `internal/worker/`
- **Config via environment** em `internal/config/`

## Consequências

- Fica fácil: performance nativa, baixo uso de memória, concorrência simples
- Fica difícil: duas linguagens no monorepo (Java + Go), deploy separado
- Risco: complexidade operacional de manter dois runtimes

## Alternativas consideradas

- **Java com Kafka Streams**: acoplaria ao backend principal
- **Node.js**: performance inferior para alto throughput
- **Python**: GIL limita concorrência real
