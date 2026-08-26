---
name: e2e-qa-skill
description: Metodologia de testes E2E pela UI real. Planejamento, execução e relatório de regressão via Browser pane. Leitura obrigatória antes de executar testes E2E.
---

# E2E QA Skill — Metodologia

> Metodologia para testes E2E navegando pela UI real do sistema.

## Ferramenta

Browser pane do Claude Code — navegação real, não simulação.

## Princípios

1. **UI real** — sempre navegar pela interface, não por API direta
2. **Fluxos completos** — do início ao fim do cenário
3. **Evidência** — registrar estado observado em cada passo
4. **Independência** — cada cenário deve funcionar isoladamente

## Cenários típicos

- Login → navegação → ação → resultado esperado
- Fluxo de compra completo
- CRUD de entidade principal
- Tratamento de erros (404, 403, validação)

## Formato de relatório

| # | Cenário | Resultado | Evidência |
|---|---------|-----------|-----------|
| 1 | <descrição> | PASS/FAIL | <estado observado> |

## Quando usar

- Após implementação de feature significativa
- Antes de merge de PR grande
- Regressão periódica
- Validação de fix de bug com impacto visual
