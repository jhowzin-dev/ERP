---
name: frontend-design
description: Design e craft de UI no OminiCore (hierarquia visual, estados, a11y, composição). Use ao desenhar ou polir telas. Não use para contratos HTTP (backend-skill) nem para regressão pela UI (e2e-qa-skill). Convenções de ficheiros ficam em frontend-skill.
---

# Frontend design (OminiCore)

Conhecimento de **interface**, não de pastas. Pastas, services e Tailwind/SCSS estão em [`frontend-skill`](../frontend-skill/SKILL.md). Implementação: agent `frontend-engineer`.

## Quando aplicar

| Situação | Aplicar |
|----------|---------|
| Hierarquia visual, densidade, estados empty/error/loading | Sim |
| a11y, foco, teclado, contraste | Sim |
| Nova página ou componente em `frontend/src` | Sim, em conjunto com `frontend-skill` |
| API Java, Kafka, Flyway | Não |

## Princípios

- Composição sobre ecrãs monolíticos; primitivos em `src/components/ui/` primeiro.
- Copy pt-BR, incluindo `sr-only`.
- Loading / error / empty / retry canónicos — sem spinner ad-hoc.
- Papel na UI não substitui RBAC no backend.

## Entrega

Validação: `cd frontend && npm run lint && npm run test && npm run build`.
