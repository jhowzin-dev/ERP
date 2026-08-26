# SDD Orchestrator — Fluxo PRD → Design → Spec/Tasks

> Executor do fluxo Spec-Driven Development. Cada fase tem um gate humano
> antes de avançar. O orchestrator é invocado como skill, não como agente.

## Visão geral

```
Fase A (PRD) ──gate──► Fase B (Design) ──gate──► Fase C (Spec) ──gate──► Fase D (Tasks) ──gate──► Fase E (Implementação)
    │                      │                       │                       │                          │
    │  PRD.md              │  design.md            │  spec.md              │  tasks.md                │  código
    │  saída: problema,    │  saída: arquitetura,  │  saída: contrato,     │  saída: tarefas          │  saída: PR ready
    │  personas, métricas  │  diagramas, decisões  │  endpoints, DTOs      │  quebradas, deps         │
    └──────────────────────┴───────────────────────┴───────────────────────┴──────────────────────────┘
```

## Fase A — PRD (Product Requirements Document)

**Quem executa**: PO
**Arquivo de saída**: `docs/features/<feature-id>/prd.md`

### Template

```markdown
---
version: 1
status: draft
---

# PRD — <Nome da Feature>

## 1. Problema
<o que resolve, por que importa agora>

## 2. Personas
<quem usa, o que faz>

## 3. Funcionalidades
<lista numerada, cada uma com Critério de Aceite>

## 4. Métricas de sucesso
<como saberemos que funcionou>

## 5. Fora de escopo
<o que NÃO faremos nesta versão>

## 6. Pendências
<[A DEFINIR] / [VALIDAR]>
```

### Gate A
- [ ] Problema definido com clareza
- [ ] Pelo menos 1 persona documentada
- [ ] Funcionalidades com critérios de aceite testáveis
- [ ] Nenhum `[A DEFINIR]` bloqueante sem resolução

---

## Fase B — Design Técnico

**Quem executa**: Tech Lead
**Arquivo de saída**: `docs/features/<feature-id>/design.md`

### Template

```markdown
---
version: 1
status: draft
---

# Design — <Nome da Feature>

## 1. Visão técnica
<resumo de 3 linhas: o que construir e como>

## 2. Arquitetura
<diagrama ou referência ao módulo afetado>

## 3. Tecnologias envolvidas
<libs, serviços externos, decisões técnicas>

## 4. Diagrama de componentes
<fluxo de dados, chamadas, integrações>

## 5. Decisões técnicas
<ADRreferenced ou decisões novas>

## 6. Riscos técnicos
<o que pode dar errado, mitigações>
```

### Gate B
- [ ] Arquitetura definida e revisada
- [ ] Tecnologias validadas (não há dependência nova sem aprovação)
- [ ] Diagrama presente ou referenciado
- [ ] Riscos listados com mitigação

---

## Fase C — Especificação

**Quem executa**: Tech Lead + Devs
**Arquivo de saída**: `docs/features/<feature-id>/spec.md`

### Template

```markdown
---
version: 1
status: draft
---

# Spec — <Nome da Feature>

## 1. Contrato de dados
<DTOs, payloads, schemas Zod, interfaces TypeScript>

## 2. Endpoints
<método, path, body, response, status codes>

## 3. Regras de validação
<campos obrigatórios, formatos, limites>

## 4. Regras de negócio
<RN-xx ou novas, com comportamento esperado>

## 5. Testes
<critérios de teste, cenários Happy Path e Edge Cases>

## 6. Integrações
<chamadas externas, webhooks, eventos>
```

### Gate C
- [ ] Contrato de dados definido (front + back concordam)
- [ ] Todos os endpoints documentados com status codes
- [ ] Regras de validação mapeadas
- [ ] Testes definidos antes do código

---

## Fase D — Tarefas

**Quem executa**: Tech Lead
**Arquivo de saída**: `docs/features/<feature-id>/tasks.md`

### Template

```markdown
---
version: 1
status: draft
---

# Tasks — <Nome da Feature>

## Legenda
- `[ ]` pendente | `[~]` em andamento | `[x]` concluído | `[-]` cancelado

## Backend
- [ ] T-001: <descrição> (~Xh)
- [ ] T-002: <descrição> (~Xh)

## Frontend
- [ ] T-003: <descrição> (~Xh)
- [ ] T-004: <descrição> (~Xh)

## Integração
- [ ] T-005: <descrição> (~Xh)

## Infra
- [ ] T-006: <descrição> (~Xh)

## Dependências
T-002 depende de T-001
T-004 depende de T-003
```

### Gate D
- [ ] Tarefas quebradas em executáveis (max ~4h cada)
- [ ] Dependências mapeadas
- [ ] Estimativas presentes
- [ ] Validação do harness definida por tarefa

---

## Fase E — Implementação

**Quem executa**: Dev Back + Dev Front
**Arquivo de referência**: `docs/features/<feature-id>/state.md`

O `state.md` é atualizado a cada conclusão de tarefa:

```markdown
---
version: 1
status: implementing
---

# State — <Nome da Feature>

## Progresso
| Fase | Status | Concluída em |
|------|--------|-------------|
| A (PRD) | done | 2026-08-20 |
| B (Design) | done | 2026-08-21 |
| C (Spec) | done | 2026-08-22 |
| D (Tasks) | implementing | — |
| E (Implementação) | — | — |

## Tarefas concluídas
- T-001: <descrição> ✅
- T-002: <descrição> ✅

## Bloqueios
<nenhum ou lista de bloqueadores>
```

---

## Modo rápido (fora do pipeline)

Perguntas informativas, pequenos ajustes de doc, ou esclarecimentos não
passam pelo SDD — responder direto. O pipeline é para **trabalho de entrega**
(feature, refactor, integração) que exige código + testes + validação.
