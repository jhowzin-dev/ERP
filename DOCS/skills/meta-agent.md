# Meta-Agent — Orquestrador de Pedidos Complexos

> Skill de orquestração. Roteia pedidos vagos ou multi-domínio para o
> especialista correto. Roda na thread principal.

## Quando invocar

- Pedido vago ou ambíguo ("fazer integração", "melhorar performance")
- Pedido que envolve múltiplos domínios (backend + frontend + infra)
- Pedido que não encaixa claramente em um agente específico

## Como funciona

1. Lê o pedido do usuário
2. Identifica o domínio(s) envolvido(s)
3. Roteia para o agente certo:
   - Regra de negócio / produto → **PO**
   - Arquitetura / técnica → **Tech Lead**
   - Código backend → **Dev Back**
   - Código frontend → **Dev Front**
   - Infra / deploy → **DevOps**
   - Validação → **QA**
   - Documentação → **DOCS**
4. Se multi-domínio, orquestra em sequência (não paralelo)

## Regras

- Não executa código — apenas roteia
- Se o pedido for claro e mono-domínio, pula o meta-agent e vai direto ao agente certo
- Sempre lê `AGENTS.md` antes de rotear
