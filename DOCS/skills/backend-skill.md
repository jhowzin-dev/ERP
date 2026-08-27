# Backend Skill — Convenções Java/Spring/Modulith

> Skill de conhecimento para o Dev Backend. Ler antes de escrever código no `backend/`.

## Contexto obrigatório

O backend é um monolito modular com Spring Boot 4.0.7 + Spring Modulith.
Cada módulo de negócio é um pacote em `backend/src/main/java/com/ominicore/backend/`.

## Stack

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| Java | 21 (JDK 21 LTS) | Runtime |
| Spring Boot | 4.0.7 | Framework |
| Spring Modulith | (via boot) | Modularidade |
| Spring Data JPA | (via boot) | Persistência |
| Flyway | (via boot) | Migrations |
| Spring Security | (via boot) | Auth |
| Spring Kafka | (via boot) | Eventos |
| PostgreSQL | 15+ | Banco |

## Estrutura de pacotes

```
backend/src/main/java/com/ominicore/backend/
├── finance/          # Financeiro
│   ├── api/          # Controllers
│   ├── internal/     # Services, repositories, entities
│   └── package-info.java
├── sales/            # Vendas
├── inventory/        # Estoque
├── customers/        # Clientes
├── production/       # Produção
├── marketplace/      # Integração ML
├── catalog/          # Catálogo de produtos
├── events/           # Eventos cross-domain
└── BackendApplication.java
```

## Convenções

- Controllers ficam em `<modulo>/api/`
- Services, repositories, entities ficam em `<modulo>/internal/`
- Um `package-info.java` em cada pacote para documentação
- Não introduzir dependências sem aval do Tech Lead
- Seguir `README.md` para decisões de stack e convenções

## Validações

```bash
.\mvnw.cmd test              # Windows
./mvnw test                  # Linux/macOS
.\harness.ps1 backend        # Harness completo
```

## Referências

- [`README.md`](../../README.md) — convenções do projeto
- [`docs/sdd/adrs/`](../sdd/adrs/) — decisões arquiteturais (ADRs)
- [`docs/features/`](../features/) — especificações por feature

