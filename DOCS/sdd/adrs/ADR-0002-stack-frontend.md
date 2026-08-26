# ADR 0002: Stack Frontend — React + Vite + Tailwind

**Status**: aceito
**Data**: 2026-08-01
**Decidido por**: Tech Lead

## Contexto

O frontend precisa de uma SPA rápida para gestão de produtos, com UI
responsiva e experiência moderna. Foco em performance e DX.

## Decisão

- **React 19** com **TypeScript** (strict mode)
- **Vite** como bundler (HMR rápido, build otimizado)
- **Tailwind CSS v4** para estilos utility-first
- **React Router v7** para roteamento SPA
- **React Query (TanStack Query)** + **axios** para state do servidor
- **React Hook Form** + **Zod** para formulários
- **react-i18next** para i18n (português como padrão)
- **oxlint** como linter (mais rápido que ESLint)

## Consequências

- Fica fácil: DX excelente, build ultra-rápido, ecossistema rico
- Fica difícil: Tailwind pode gerar classes冗antas, learning curve para quem não conhece
- Risco: React 19 pode ter APIs instáveis (useFormStatus, etc.)

## Alternativas consideradas

- **Next.js**: SSR desnecessário para este caso (SPA interna)
- **Vue/Nuxt**: menos experiência no time
- **Angular**: bundle maior, curva de aprendizado mais íngreme
