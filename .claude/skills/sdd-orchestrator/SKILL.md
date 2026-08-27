---
name: sdd-orchestrator
description: Executor do fluxo Spec-Driven Development (PRD → design → spec → tasks). Use para features novas que precisam de planejamento completo antes do código. Cada fase tem um gate humano antes de avançar. Não use para bugs, ajustes pequenos ou pedidos mono-domínio simples.
---

# SDD Orchestrator

**Habilidade de orquestração**: executa o fluxo SDD. Roda na thread principal (tem acesso à ferramenta Agent).

---

## 1. Quando aplicar

| Situação | Aplicar |
| -------- | ------- |
| Feature nova que precisa de planejamento completo | Sim |
| Refactor significativo que impacta múltiplos módulos | Sim |
| Integração nova (ex: novo marketplace) | Sim |
| Bug simples ou ajuste pontual | **Não** — usar [`debug-specialist`](../debug-specialist/SKILL.md) |
| Melhoria de performance pontual | **Não** — usar [`performance-optimizer`](../performance-optimizer/SKILL.md) |
| Pedido claro e mono-domínio | **Não** — usar agent específico |

---

## 2. Ligações

| Recurso | Path |
| ------- | ---- |
| Governo SDD completo | [`docs/sdd/SDD-ORCHESTRATOR.md`](../../../docs/sdd/SDD-ORCHESTRATOR.md) |
| Templates de prompt | [`docs/sdd/SDD-USAGE-GUIDE.md`](../../../docs/sdd/SDD-USAGE-GUIDE.md) |
| ADRs | [`docs/sdd/adrs/`](../../../docs/sdd/adrs/) |
| Features ativas | [`docs/features/`](../../../docs/features/) |
| Backend (convenções) | [`backend-skill`](../backend-skill/SKILL.md) |
| Frontend (convenções) | [`frontend-skill`](../frontend-skill/SKILL.md) |

---

## 3. Fluxo

```
Fase A (PRD) ──gate──► Fase B (Design) ──gate──► Fase C (Spec) ──gate──► Fase D (Tasks) ──gate──► Fase E (Implementação)
    │                      │                       │                       │                          │
    │  prd.md              │  design.md            │  spec.md              │  tasks.md                │  código
    │  saída: problema,    │  saída: arquitetura,  │  saída: contrato,     │  saída: tarefas          │  saída: PR ready
    │  personas, métricas  │  diagramas, decisões  │  endpoints, DTOs      │  quebradas, deps         │
    └──────────────────────┴───────────────────────┴───────────────────────┴──────────────────────────┘
```

---

## 4. Arquivos de saída

Cada feature vive em `docs/features/<feature-id>/`:

| Fase | Arquivo | Quem executa | Conteúdo |
|------|---------|-------------|----------|
| A | `prd.md` | PO | Problema, personas, funcionalidades, métricas |
| B | `design.md` | java-architect | Arquitetura, diagramas, decisões técnicas |
| C | `spec.md` | java-architect + implementers | Contrato de dados, endpoints, validações |
| D | `tasks.md` | java-architect | Tarefas quebradas, dependências, estimativas |
| E | código | implementers | PR ready para review |

---

## 5. Gates

### Gate A (PRD)
- [ ] Problema definido com clareza
- [ ] Pelo menos 1 persona documentada
- [ ] Funcionalidades com critérios de aceite testáveis
- [ ] Nenhum `[A DEFINIR]` bloqueante sem resolução

### Gate B (Design)
- [ ] Arquitetura definida e revisada
- [ ] Tecnologias validadas (dependência nova aprovada)
- [ ] Diagrama presente ou referenciado
- [ ] Riscos listados com mitigação

### Gate C (Spec)
- [ ] Contrato de dados definido (front + back concordam)
- [ ] Todos os endpoints documentados com status codes
- [ ] Regras de validação mapeadas
- [ ] Testes definidos antes do código

### Gate D (Tasks)
- [ ] Tarefas quebradas em executáveis (max ~4h cada)
- [ ] Dependências mapeadas
- [ ] Estimativas presentes
- [ ] Validação do harness definida por tarefa

---

## 6. Processo

1. **Identificar fase atual** — onde o usuário está no fluxo?
2. **Validar gate anterior** — a fase anterior foi concluída?
3. **Gerar template** — output formatado para a fase.
4. **Aguardar aprovação** — gate é humano, nunca automático.
5. **Avançar** — apenas após aprovação explícita.

---

## 7. Como invocar

### Pelo orchestrator (recomendado)

```
Siga o SDD-ORCHESTRATOR.md. Estou na Fase A (PRD) para a feature <nome>.
O problema é <descrição curta>. As personas são <lista>. Crie o template prd.md.
```

### Prompts por fase

**Fase A (PRD):**
```
Siga o SDD-ORCHESTRATOR.md. Fase A (PRD) para <feature-id>.
Problema: <descrição>. Personas: <lista>. Crie prd.md.
```

**Fase B (Design):**
```
Siga o SDD-ORCHESTRATOR.md. Fase B (Design) para <feature-id>.
PRD em docs/features/<feature-id>/prd.md. Crie design.md.
```

**Fase C (Spec):**
```
Siga o SDD-ORCHESTRATOR.md. Fase C (Spec) para <feature-id>.
Design em docs/features/<feature-id>/design.md. Crie spec.md.
```

**Fase D (Tasks):**
```
Siga o SDD-ORCHESTRATOR.md. Fase D (Tasks) para <feature-id>.
Spec em docs/features/<feature-id>/spec.md. Crie tasks.md.
```

---

## 8. state.md — Status vivo

Atualizar sempre que:
- Uma fase é concluída (gate passou).
- Uma tarefa é marcada como concluída.
- Um bloqueio é identificado ou resolvido.

---

## 9. Modo rápido (fora do pipeline)

Perguntas informativas, pequenos ajustes de doc, ou esclarecimentos não passam pelo SDD — responder direto. O pipeline é para **trabalho de entrega** (feature, refactor, integração) que exige código + testes + validação.

---

## 10. Anti-padrões

| Evitar | Porquê |
| ------ | ------ |
| Aprovar gate automaticamente | Gate é humano; o orchestrator só valida critérios |
| Pular fase | Cada fase tem dependência da anterior |
| Gerar código antes da spec | Viola o princípio SDD |
| Não atualizar state.md | Perde-se rastreabilidade |
| Criar feature sem ID | Impossível organizar artefatos |

---

## Histórico

| Versão | Mudança |
| ------ | ------- |
| 3.0.0 | Movida para `.claude/skills/` (passa a ser carregável); formato alinhado ao EmpregaNetAPI |
| 2.0.0 | Expansão: gates detalhados, prompts, anti-padrões |
| 1.0.0 | Versão inicial básica |
