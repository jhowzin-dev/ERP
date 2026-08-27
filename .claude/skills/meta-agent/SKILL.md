---
name: meta-agent
description: Roteador de pedidos vagos, ambíguos ou multi-domínio. Analisa o pedido, identifica domínios envolvidos e delega para o agent correto. Use quando o pedido não se encaixa claramente em um único agent, quando envolve múltiplos módulos ou quando a intenção é ambígua. Não use para pedidos claros e mono-domínio — vá direto ao agent específico.
---

# Meta-Agent — Roteador

**Habilidade de orquestração**: roteia pedidos para o agent certo. Roda na thread principal (tem acesso à ferramenta Agent).

---

## 1. Quando aplicar

| Situação | Aplicar |
| -------- | ------- |
| Pedido vago ou ambíguo ("fazer integração", "melhorar performance") | Sim |
| Pedido que envolve múltiplos domínios (backend + frontend + infra) | Sim |
| Pedido que não encaixa claramente em um agent específico | Sim |
| Pedido claro e mono-domínio | **Não** — ir direto ao agent |
| Feature nova completa (SDD) | **Não** — usar [`sdd-orchestrator`](../sdd-orchestrator/SKILL.md) |

---

## 2. Ligações

| Recurso | Path |
| ------- | ---- |
| Mapa completo de agents | [`docs/agents/README.md`](../../../docs/agents/README.md) |
| Skills de conhecimento | [`docs/skills/README.md`](../../../docs/skills/README.md) |
| Governo SDD | [`docs/sdd/SDD-ORCHESTRATOR.md`](../../../docs/sdd/SDD-ORCHESTRATOR.md) |

---

## 3. Mapa de roteamento

| Domínio do pedido | Agent | Skill associada |
| ----------------- | ----- | ---------------- |
| Arquitetura, padrões, fronteiras | `java-architect` | `backend-skill` |
| Código backend Java/Spring | `java-implementer` | `backend-skill` |
| Código frontend React/Vite | `frontend-engineer` | `frontend-skill` |
| Testes automatizados | `test-engineer` | — |
| Debug, causa raiz | `debug-specialist` | — |
| Performance, gargalos | `performance-optimizer` | — |
| Revisão de código, PR | `code-reviewer` | — |
| QA End-to-End pela UI | `e2e-qa-engineer` | `e2e-qa-skill` |
| Feature nova (SDD completo) | `sdd-orchestrator` | `sdd-orchestrator` |
| Infra, Docker, CI/CD | `java-architect` (read-only) | — |

---

## 4. Processo

1. **Ler o pedido** do usuário com atenção.
2. **Identificar domínios** envolvidos (backend? frontend? infra? produto?).
3. **Classificar**:
   - **Mono-domínio claro** → delegar direto ao agent.
   - **Multi-domínio** → orquestrar em sequência (não paralelo).
   - **Vago/ambíguo** → clarificar com o usuário antes de delegar.
4. **Delegar** com contexto suficiente para o agent.
5. **Acompanhar** e encadear se necessário.

---

## 5. Decisões de roteamento

### Pedido claro e mono-domínio

"Adicionar validação de SKU no controller de produtos" → `java-implementer`

### Pedido multi-domínio

"Implementar tela de produtos com criação, edição e exclusão" → sequência: `java-implementer` (API) → `frontend-engineer` (UI) → `test-engineer` (testes)

### Pedido vago

"Melhorar o sistema" → Perguntar: "O que especificamente? Performance? UX? Manutenção?"

### Feature nova

"Implementar módulo de promoções" → `sdd-orchestrator` (fluxo SDD completo)

---

## 6. Regras

| Regra | Detalhe |
| ----- | ------- |
| **Não executar código** | Meta-agent apenas roteia, nunca implementa |
| **Se claro, pular** | Se o pedido é mono-domínio e claro, não usar meta-agent |
| **Ler CLAUDE.md** | Contexto obrigatório antes de rotear |
| **Sequencial** | Multi-domínio: um agent de cada vez, encadeando resultados |
| **Contexto mínimo** | Passar ao agent apenas o que ele precisa saber |
| **Human-in-the-loop** | Decisões de risco ficam com o humano |

---

## 7. Anti-padrões

| Evitar | Porquê |
| ------ | ------ |
| Rotear pedidos claros e mono-domínio | Overhead desnecessário |
| Executar código dentro do meta-agent | Violação de responsabilidade |
| Paralelizar agents | Risco de conflitos; preferir sequencial |
| Não ler CLAUDE.md antes de rotear | Falta de contexto |
| Passar contexto excessivo ao agent | Poluição de memória |

---

## 8. Validação

O meta-agent não tem comandos próprios. A validação é indireta:
- O agent destino executa seus próprios comandos.
- O resultado é avaliado pelo usuário ou pelo `code-reviewer`.

---

## Histórico

| Versão | Mudança |
| ------ | ------- |
| 3.0.0 | Movida para `.claude/skills/` (passa a ser carregável); formato alinhado ao EmpregaNetAPI |
| 2.0.0 | Expansão: mapa de roteamento, processo, anti-padrões |
| 1.0.0 | Versão inicial básica |
