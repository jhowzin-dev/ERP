---
name: frontend-skill
description: Convenções canónicas do frontend React/Vite/Tailwind do OminiCore — componentes, hooks, services, SCSS Modules, react-query, i18n, auth/RBAC. Use ao ler, escrever ou revisar qualquer coisa em frontend/src, incluindo páginas, componentes, hooks, cliente HTTP, estilos e acessibilidade. Não use para backend Java/Spring (backend-skill) nem para regressão pela UI real (e2e-qa-skill).
---

# Frontend (React/Vite/Tailwind — OminiCore)

Base de **conhecimento** do frontend: decisões fechadas, armadilhas já pagas em produção e checklists.
O comportamento de implementação está no agent `frontend-engineer`, que carrega esta skill como contexto obrigatório.

---

## 1. Quando aplicar

| Situação | Aplicar |
| -------- | ------- |
| Todo o trabalho em `frontend/src/` | Sim |
| Novas páginas, componentes, hooks, services, estilos | Sim |
| Integração com a API + validação ao renderizar dados | Sim |
| Refactors que dividem componentes grandes ou corrigem a11y | Sim |
| Handlers, entidades, contratos do lado do servidor Java | Não — [`backend-skill`](../backend-skill/SKILL.md) |
| Validar o comportamento real navegando a UI | Não — [`e2e-qa-skill`](../e2e-qa-skill/SKILL.md) |

---

## 2. Ligações

| Recurso | Path |
| ------- | ---- |
| Mapa do monorepo e comandos de build | [`docs/README.md`](../../../docs/README.md) |
| Agent de implementação frontend | [`frontend-engineer`](../../agents/frontend-engineer.md) |
| Paridade de contratos com a API | [`backend-skill`](../backend-skill/SKILL.md) |
| Governo SDD (quando há pasta `docs/features/<id>/`) | [`docs/sdd/SDD-ORCHESTRATOR.md`](../../../docs/sdd/SDD-ORCHESTRATOR.md) |

---

## 3. Princípios

| Princípio | Prática obrigatória |
| --------- | ------------------- |
| **SRP nos componentes** | Componente faz **uma** parcela óbvia de UI; dados/efeitos vão para hooks/services. |
| **Backend é fonte de verdade** | Não re-implementar regras densas já garantidas pela API; duplicação só para ergonomia, com paridade de tipos na fronteira. |
| **Inversão de dependência na fronteira** | Páginas/hooks chamam o `service/` da feature dona — sem `fetch`/axios disperso em componentes. |
| **KISS/YAGNI** | Não criar camadas profundas antes de haver comportamento repetido com valor claro — mas isolá-lo **antes** da segunda duplicação real. |
| **Type safety** | TypeScript `strict`; **proibido `any`**; `unknown` + narrowing quando necessário. |

---

## 4. Stack (fechamento explícito)

| Usar | Não usar neste projecto |
| ---- | ----------------------- |
| React 19 + Vite 8 + TypeScript strict | Outro CSS framework além do Tailwind v4 |
| Tailwind v4 para estilos utilitários | SCSS Modules misturados com Tailwind na mesma regra |
| TanStack Query 5 para state do servidor | `useEffect` + `useState` para fetch de dados |
| React Hook Form 7 + Zod 4 para formulários | Validação só no submit sem mensagens tratadas |
| Axios 1.x para HTTP client | `fetch` nativo espalhado sem interceptors |
| react-i18next 17 para internacionalização | Textos hardcoded em português |

---

## 5. Pastas e responsabilidades

| Camada lógica | Onde | Regra |
| ------------- | ---- | ----- |
| UI pura ("dumb") | `src/components/ui/` | Só props/handlers declarados; sem side-effects escondidos |
| Coesão por feature | `src/features/<domínio>/` | Colocar hooks, services e componentes locais junto |
| API + schemas | `src/features/<domínio>/services/` — `*-api.ts`, `*-schema.ts`, `*-queries.ts` | Zod no primeiro contacto com o JSON entrante |
| Infra transversal | `src/api/` (axios + interceptors), `src/hooks/` (globais) | Não duplicar cliente HTTP por feature |
| Moldura da aplicação | `src/pages/`, `src/routes/` | Shell único para rotas públicas e autenticadas |
| Helpers de UI cross-feature | Só com **3+ consumidores** confirmados | Senão, duplicação controlada até estabilizar |

> `src/services/` não existe mais — o service vive na feature dona. Infra compartilhada em `src/api/`.

**Features existentes:** `catalog`, `inventory`, `sales`, `finance`, `customers`, `dashboard`, `marketplace`.

---

## 6. Componentes — práticas

- **PascalCase** para componentes (arquivo e export).
- **camelCase** para hooks (`useXxx`).
- **camelCase** para services (arquivo) com exports nomeados.
- Componentes de função (não class).
- `forwardRef` quando necessário.
- **i18n** para todos os textos visíveis — nunca hardcodar strings em português no JSX.
- **Co-localização:** componente, teste e estilo ficam juntos quando específico de uma feature.
- Componentes em `components/ui/` são reutilizáveis; componentes em `features/` são específicos da feature.

---

## 7. SCSS Modules e Tailwind

- **Tailwind v4** para estilos utilitários (spacing, flex, grid, responsive).
- **SCSS Modules** para estilos complexos específicos de componente (`*.module.scss`).
- Variáveis globais em `styles/_variables.scss`.
- **Não** misturar Tailwind e SCSS Modules na mesma regra de estilo.
- Utility classes do Tailwind para layout; SCSS para componentes com estados complexos.

---

## 8. Estado, dados e comunicação com o servidor

| Tópico | Expectativa |
| ------ | ----------- |
| **Loading / error / empty** | Sempre tratados visualmente, com retry onde a UX exigir |
| **Mutations idempotentes** | Evitar POST duplo: desabilitar botão progressivamente, debounce |
| **Optimistic UI** | Só com caminho compensatório em caso de falha — nunca esconder erros |
| **Stale time** | `staleTime` definido para queries (ex: 5 minutos para listagens) |

---

## 9. Autenticação e RBAC

- **Auth por cookie httpOnly** — nenhum token em JS. O interceptor lê o cookie e renova automaticamente.
- **Rota nova exige** actualizar `isPublicPath` / `canAccessPath`; forbidden vai para página de não autorizado.
- **Capacidades** centralizadas; sem strings mágicas espalhadas — extrair enums/helpers compartilhados.
- UI condicional (menus/acções) coerente com o papel real vindo do backend — **nunca** apenas esconder o link.

---

## 10. Testes

### Infra real hoje

O frontend usa **Vitest** + **React Testing Library** para testes de componente e **MSW** para mock de API.

```bash
cd frontend && npm run test
```

### Hierarquia de valor

| Prioridade | Foco |
| ---------- | ---- |
| 1º | Lógica pura de alto risco: schemas Zod, mappers, regras de negócio, controlo de acesso a rotas |
| 2º | Fluxos de formulário (validação → payload da API) como cenários de integração |
| 3º | Comportamento que só aparece com a app a correr (navegação real, layout, timing) → **não é Vitest**: é a regressão manual pela UI, coberta por [`e2e-qa-skill`](../e2e-qa-skill/SKILL.md) |

**Testing Library, Cypress e Playwright NÃO estão instalados.** Não escrever testes que os assumam nem sugeri-los como se existissem; propor a adição é decisão explícita.

---

## 11. Validação (comandos reais)

```bash
cd frontend && npm run lint
cd frontend && npm run test
cd frontend && npm run build
.\harness.ps1 frontend        # Harness completo
```

---

## 12. Checklist de entrega (feature UI)

1. [ ] Pasta de feature coesa; componentes suficientemente pequenos.
2. [ ] `services/` da feature com Zod na fronteira — entrada **e** payload de saída.
3. [ ] Estados **loading/error/empty/retry** tratados visualmente — sem spinner ad-hoc.
4. [ ] Form com RHF + Zod e mensagens ao utilizador em **pt-BR**.
5. [ ] a11y: navegação por teclado, foco em overlays, `prefers-reduced-motion`.
6. [ ] Rota nova → rotas públicas/autenticadas actualizadas; proxy e guard consistentes.
7. [ ] `lint` + `test` + `build` verdes (§11).
8. [ ] Cenários de teste criados/actualizados quando há lógica pura nova.

---

## 13. Anti-padrões

| Bloqueado | Motivo |
| --------- | ------ |
| Lógica de negócio densa no JSX | Impede reuso e teste isolado |
| `any` em TypeScript | `strict` é regra do projecto |
| `fetch`/axios espalhado sem service | Regressão rápida de contratos inconsistentes |
| Spinner/skeleton ad-hoc | Já existem componentes canónicos no projeto |
| Token de auth em JS / `js-cookie` para sessão | A API já emite httpOnly; duplicar cria cookie fantasma |
| Texto de UI hardcoded em português | Usar i18n para todos os textos visíveis |
| `useEffect` + `useState` para fetch de dados | Usar TanStack Query |
| CSS framework diferente do Tailwind | Política actual explícita |

---

## 14. Idioma

Copy de utilizador final em **português (Brasil)**; identificadores de código em **inglês**.

---

## Histórico

| Versão | Mudança |
| ------ | ------- |
| 3.0.0 | Movida para `.claude/skills/` (passa a ser carregável); separada de comportamento (agents); formato alinhado ao EmpregaNetAPI |
| 2.0.0 | Expansão: seções completas, anti-padrões, checklist |
| 1.0.0 | Versão inicial básica |
