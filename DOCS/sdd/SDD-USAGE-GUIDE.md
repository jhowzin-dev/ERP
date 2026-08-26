# SDD Usage Guide

> Guia de uso do fluxo Spec-Driven Development. Templates de prompt,
> versionamento, e como o orchestrator é invocado.

## Como invocar o SDD

### Pelo orchestrator (recomendado)

O orchestrator é uma **skill** — carregada automaticamente pela `description`
ou invocada por `/sdd-orchestrator`. Ele:

1. Pergunta em qual fase está
2. Valida os critérios de gate
3. Gera o template correto para a fase
4. Aguarda aprovação humana antes de avançar

### Pelo agent (quando o pedido é largo)

Se o pedido for uma feature nova, o pipeline completo é:

```
PO.md → TECH_LEAD.md → DEV_BACK.md / DEV_FRONT.md → QA.md
```

Cada etapa lê a saída da anterior e a transforma.

## Versionamento

Cada artefato SDD tem `frontmatter` com versão e status:

```yaml
---
version: 1
status: draft | in-review | approved | implementing | done
---
```

Regras:
- `version` começa em 1 e incrementa a cada revisão significativa
- `status` avança: `draft` → `in-review` → `approved` → `implementing` → `done`
- `blocked` é um status especial (usar quando há `[A DEFINIR]` sem resolução)

## state.md — Status vivo

O `state.md` é o **status em tempo real** da feature. Atualizar sempre que:
- Uma fase é concluída (gate passou)
- Uma tarefa é marcada como concluída
- Um bloqueio é identificado ou resolvido

## Prompts úteis

### Criar PRD
```
Siga o SDD-ORCHESTRATOR.md. Estou na Fase A (PRD) para a feature <nome>.
O problema é <descrição curta>. As personas são <lista>. Crie o template prd.md.
```

### Criar Design
```
Siga o SDD-ORCHESTRATOR.md. Fase B (Design) para <feature-id>.
O PRD está em docs/features/<feature-id>/prd.md. Crie o design.md.
```

### Criar Spec
```
Siga o SDD-ORCHESTRATOR.md. Fase C (Spec) para <feature-id>.
O design está em docs/features/<feature-id>/design.md. Crie o spec.md.
```

### Criar Tasks
```
Siga o SDD-ORCHESTRATOR.md. Fase D (Tasks) para <feature-id>.
A spec está em docs/features/<feature-id>/spec.md. Crie o tasks.md.
```

## Gates

Cada gate é validado pelo orchestrator. Se falhar, o orchestrator:
1. Lista o que falta
2. Sugere o que corrigir
3. Aguarda correção antes de gerar o template da próxima fase

O gate é **humano** — o orchestrator não aprova automaticamente.
