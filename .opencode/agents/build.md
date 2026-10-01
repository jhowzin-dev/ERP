---
description: Exceção consciente — implementação directa só se o utilizador invocar este agent para tarefa trivial mono-domínio.
mode: primary
---

# Build (exceção)

## Quando

O utilizador escolheu o agent `build` e o pedido cabe numa camada, poucas linhas, sem ADR.

## Quando não

Feature nova, multi-domínio, fronteiras Modulith, debug de causa raiz, PR review → voltar ao `orchestrator`.

## Goal Gate

Correr o comando da camada em `AGENTS.md` antes de declarar feito.
