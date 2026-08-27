---
name: backend-skill
description: Convenções canónicas do backend Java/Spring do OminiCore — Spring Modulith, camadas por domínio (api/internal), Flyway, Kafka, contrato HTTP camelCase, testes JUnit 5/Mockito com fixture H2 in-memory. Use ao ler, escrever ou revisar qualquer coisa em backend/src ou backend/tests, ou ao definir contratos HTTP consumidos pelo frontend. Não use para trabalho de UI (frontend-skill) nem para especificação de feature antes de código (sdd-orchestrator).
---

# Backend (Java/Spring — OminiCore API)

Base de **conhecimento** do backend: fatos do repositório, regras de camada, testes e anti-padrões.
Não é um perfil de comportamento — o comportamento está nos agents `java-architect` e `java-implementer`,
que carregam esta skill como contexto obrigatório.

---

## 1. Quando aplicar

| Situação | Aplicar |
| -------- | ------- |
| Alterações em `backend/src/` (módulos domain, api, internal) | Sim |
| Novos controllers, services, repositories, entities, migrations | Sim |
| Testes em `backend/tests/` (Unit ou Integration) | Sim |
| Contratos HTTP consumidos pelo frontend | Sim |
| UI, hooks, estilos | Não — [`frontend-skill`](../frontend-skill/SKILL.md) |
| Especificar feature antes de código | Não — [`sdd-orchestrator`](../sdd-orchestrator/SKILL.md) |

---

## 2. Ligações

| Recurso | Path |
| ------- | ---- |
| Mapa do monorepo e comandos de build | [`docs/README.md`](../../../docs/README.md) |
| Fronteiras e decisões estruturais | [`java-architect`](../../agents/java-architect.md) |
| Código Java concreto | [`java-implementer`](../../agents/java-implementer.md) |
| Governo SDD (fases e gate) | [`docs/sdd/SDD-ORCHESTRATOR.md`](../../../docs/sdd/SDD-ORCHESTRATOR.md) |
| ADRs transversais | [`docs/sdd/adrs/`](../../../docs/sdd/adrs/) |

Para features com pasta de spec activa (`docs/features/<id>/`): respeitar `prd.md` / `design.md`
antes de divergir; registar desvios pragmáticos nas *deviation notes* do `tasks.md`.

---

## 3. Princípios

| Princípio | Como se traduz aqui |
| --------- | ------------------- |
| **Domínio no centro** | Regras e invariantes no módulo; nomenclatura alinhada à linguagem de negócio. |
| **Menos poder útil** | KISS/YAGNI: um service por responsável; não adicionar camadas "para o futuro". |
| **SOLID / coesão** | Tipos pequenos com responsabilidade clara; DRY só quando a duplicação tiver custo real. |
| **Testabilidade** | Services com colaboradores mockáveis no Unit; fluxos via application context no Integration. |
| **Fonte única de contratos** | Mudança de contrato HTTP acompanha o consumidor (frontend) quando o incremento assim o define. |

---

## 4. Camadas (`backend/src/main/java/com/ominicore/backend/`)

| Camada | Papel | Regras de dependência |
| ------ | ----- | --------------------- |
| **`<modulo>/api/`** | Controllers REST, endpoints finos | Delega sempre para internal/ |
| **`<modulo>/internal/`** | Services, repositories, entities | Não expõe para fora do módulo |
| **`events/`** | Eventos cross-domain Kafka | Producer/consumer por módulo |

**Modulith (crítico):** Comunicação entre módulos de negócio **apenas via eventos Kafka** ou injecção controlada via Spring Modulith. **Não** criar dependências diretas entre módulos de negócio diferentes.

**Módulos existentes:** `catalog`, `inventory`, `sales`, `finance`, `customers`, `production`, `marketplace`.

---

## 5. Convenções de código

- **Fluxo típico:** Controller → Service → Repository → Entity.
- **Validação:** Bean Validation (`@Valid`) nos controllers; services recebem DTOs já validados.
- **`@Transactional`:** sempre em services; eventos publicados após commit.
- **Soft delete:** `isDeleted` + `deletedAt` em vez de DELETE físico.
- **Naming de módulos:** pacote em lowercase (`catalog`, `inventory`); controller plural (`ProdutosController`).
- **Excepções de negócio:** usar classes específicas (ex: `ProdutoNaoEncontradoException`) em vez de genéricas.
- **Logging:** mensagens de negócio em português (Brasil); identificadores de código em inglês.

Se um módulo tiver estrutura ligeiramente diferente da "ideal": **preservar o padrão local**;
refactor estrutural só com tarefa explícita ou ADR quando for transversal.

---

## 6. Flyway

- Migrations em `src/main/resources/db/migration/`.
- Naming: `V{timestamp}_{descricao}.sql` (ex: `V20260826120000_create_catalog_tables.sql`).
- Release com `rename`/`drop` é **forward-only** — o canário aplica as migrações e rollback não recupera dados. Planear migração em duas fases (adicionar → migrar dados → remover num release posterior).
- Alterações ao modelo (entities) acompanhadas de migrations e revisão humana antes de produção.

---

## 7. Kafka (eventos cross-domain)

- Producers: publicar eventos após commit (`@TransactionalEventListener`).
- Consumers: idempotentes para reprocessamento/retries.
- Não aplicar Saga / Outbox / Event Sourcing por moda — apenas com requisito explícito e ADR.
- Formato de payload: DTO serializado em JSON com `eventType` e `timestamp`.

---

## 8. API HTTP

- Serialização **camelCase** (Jackson default).
- Formato de erro padronizado:
  - Validação (400): `{ statusCode, code: "VALIDATION_ERROR", message, details[] }`
  - Não encontrado (404): `{ statusCode, code: "NOT_FOUND", message }`
  - Conflito (409): `{ statusCode, code: "CONFLICT", message }`
  - Não autorizado (401): `{ statusCode, code: "UNAUTHORIZED", message }`
  - Proibido (403): `{ statusCode, code: "FORBIDDEN", message }`
- **Endpoints por módulo:** `/api/{modulo}/{recurso}` (ex: `/api/catalog/produtos`).
- **Secrets** apenas em variáveis de ambiente; nunca no repositório.
- Inputs sempre validados na fronteira; endpoints sensíveis com RBAC explícito.

---

## 9. Testes (`backend/tests/`)

### Stack real deste repositório

| Componente | Uso |
| ---------- | --- |
| JUnit 5 | Framework de testes |
| Mockito | Duplos de colaboradores em Unit tests |
| Spring Boot Test | Testes de integração |
| H2 | Banco em memória para testes (in-memory) |

### Unit

- Um test por cenário; nome descritivo em inglês.
- **Mocks** para repositories e services externos.
- Cobrir não só sucesso: caminhos de validação, conflito e não autorizado.
- Prefixo: `*_Test` ou `*_test`.

### Integration

- `@SpringBootTest` com Application Context.
- Testes de endpoint via `MockMvc`.
- H2 para testes rápidos; PostgreSQL para validação final.
- **Limitação do H2 a declarar sempre que for relevante:** não reproduz constraints, semântica de provider real nem migrations. Comportamento dependente do PostgreSQL não é validável aí.
- Prefixo: `*_IT` ou `*_IntegrationTest`.

---

## 10. Validação (comandos reais)

```bash
.\mvnw.cmd test              # Windows
./mvnw test                  # Linux/macOS
.\mvnw.cmd verify            # Inclui checkstyle e testes
.\harness.ps1 backend        # Harness completo
```

---

## 11. Checklist de entrega (feature API)

1. [ ] Controller + Service + Repository seguindo o padrão existente.
2. [ ] Validações com Bean Validation coerentes com o contrato.
3. [ ] Responses em camelCase; formato de erro padronizado (§8).
4. [ ] Migrations Flyway quando o modelo mudar, com plano forward-only se houver `rename`/`drop`.
5. [ ] Unit tests nos services críticos; Integration quando tocar pipeline real (persistência).
6. [ ] Sem referências de internal a tipos de outro módulo; sem `@Autowired` disperso.
7. [ ] `./mvnw verify` verde (§10).

---

## 12. Anti-padrões

| Evitar | Porquê |
| ------ | ------ |
| Lógica de negócio gorda em controllers | Viola a segregação de responsabilidades |
| `try/catch` genérico que mascara stack | Bugs silenciosos |
| Dependências diretas entre módulos | Quebra a modularidade do Modulith |
| Repository genérico sem necessidade | Ruído e acoplamento inútil |
| Testes sem assert | Testes que nunca falham são inúteis |
| Defaults sem motivo | `null` tem semântica; defaults ocultam erros |
| Commit de migration renomeada | O history vira uma bagunça; adicionar nova migration |
| Service que depende de outro service do mesmo módulo | Possible circular dependency |

---

## 13. Idioma

Mensagens de utilizador e logs de negócio: **português (Brasil)**. Identificadores de código: **inglês**.

---

## Histórico

| Versão | Mudança |
| ------ | ------- |
| 3.0.0 | Movida para `.claude/skills/` (passa a ser carregável); separada de comportamento (agents); formato alinhado ao EmpregaNetAPI |
| 2.0.0 | Expansão: seções completas, anti-padrões, checklist |
| 1.0.0 | Versão inicial básica |
