---
name: backend-skill
description: Convenções Java/Spring/Modulith do OminiCore. Camadas, Flyway, Kafka, contrato HTTP, testes. Leitura obrigatória antes de escrever código backend.
---

# Backend Skill — Convenções Java/Spring/Modulith

> Skill de conhecimento para agents backend. Ler antes de escrever código em `backend/`.

## Stack

| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| Java | 25 (JDK 25 LTS) | Runtime |
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
- Um `package-info.java` em cada pacote
- Não introduzir dependências sem aval do architect
- Spring Modulith para comunicação entre módulos

## Validações

```bash
.\mvnw.cmd test              # Windows
./mvnw test                  # Linux/macOS
.\harness.ps1 backend        # Harness completo
```


