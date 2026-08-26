# Backend Skill — Convenções Java/Spring/Modulith

> Skill de conhecimento para o Dev Backend. Ler antes de escrever código no `backend/`.

## Contexto obrigatório

O backend é um monolito modular com Spring Boot 4.0.7 + Spring Modulith.
Cada módulo de negócio é um pacote em `backend/src/main/java/com/sgmultidia/backend/`.

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
backend/src/main/java/com/sgmultidia/backend/
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
- Seguir `ARQUITETURA/01-stack.md` para decisões de stack

## Validações

```bash
.\mvnw.cmd test              # Windows
./mvnw test                  # Linux/macOS
.\harness.ps1 backend        # Harness completo
```

## Referências

- `DOCS/SISTEMA DE GESTAO/ARQUITETURA/01-stack.md` — decisões de stack
- `DOCS/SISTEMA DE GESTAO/ARQUITETURA/02-arquitetura.md` — padrões
- `DOCS/SISTEMA DE GESTAO/ARQUITETURA/Referencias/bibliotecas.md` — libs
