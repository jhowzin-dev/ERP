# ADR 0001: Stack Backend — Java + Spring Boot + Modulith

**Status**: aceito
**Data**: 2026-08-01
**Decidido por**: Tech Lead

## Contexto

O OminiCore precisa de uma API robusta para gerenciar catálogo de produtos,
estoque, pedidos e integração com Mercado Livre. O time tem experiência com
Java e ecossistema Spring.

## Decisão

- **Java 21** (JDK 21 LTS) com **Spring Boot 4.0.7**
- **Spring Modulith** para organização modular (pacotes por domínio)
- **Maven** como build tool
- **Flyway** para migrations
- **Spring Data JPA** + **Hibernate** para persistência
- **Kafka** para eventos assíncronos (outbox pattern)
- **Spring Security** para autenticação/autorização
- **PostgreSQL** como banco relacional

## Consequências

- Fica fácil: modularidade natural, ecossistema maduro, testes integrados
- Fica difícil: JDK 25 pode ter limitações de ferramentas, complexidade do Spring
- Risco: dependência pesada do Spring (vendor lock-in moderado)

## Alternativas consideradas

- **Quarkus**: mais leve, mas menos maturidade no time
- **.NET**: experiência menor no time, ecossistema diferente
- **Node.js/NestJS**: inadequado para cargas de processamento pesado

