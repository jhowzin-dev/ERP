# Fluxo de Trabalho entre Agentes

> Protocolo completo da hierarquia de agentes do SG-MULTIDIA. Documento de
> referência — o operador (você) segue esta sequência manualmente.

## Hierarquia

```
1. PO (PO.md)            — cérebro: produto, regras de negócio, divisão da tarefa
2. Tech Lead (TECH_LEAD.md) — plano técnico, arquitetura, arquivos exatos
3. Dev Front (DEV_FRONT.md) — camada visual (frontend/)
   Dev Back (DEV_BACK.md)  — servidor (backend/ + ingestion/)
4. QA (QA.md)            — gate: harness + critérios de aceite → PASS/FAIL
5. DOCS (DOCS.md)        — documentação: clareza, estrutura, links (sob demanda)
```

## Sequência operacional

### Etapa 1 — PO

1. Operador informa o pedido/ideia.
2. PO lê `AGENTS.md` → `AGENTES/mapa-projeto.md` → seção relevante do vault.
3. PO preenche `AGENTES/tarefa.md` (campos obrigatórios, RNs, divisão front/back,
   critérios de aceite).
4. **Gate**: se existir `[A DEFINIR]` pendente → voltar ao operador. Se `[VALIDAR]`
   → confirmar antes de prosseguir.
5. Handoff para o Tech Lead.

### Etapa 2 — Tech Lead

1. Lê a tarefa do PO.
2. Consulta `ARQUITETURA/01-stack.md`, `02-arquitetura.md`,
   `Referencias/bibliotecas.md` e o código real (leitura).
3. Define arquivos exatos por parcela + contrato de dados.
4. **Gate**: se o contrato front/back não estiver definido, definir agora.
5. Handoff das parcelas para Dev Front e/ou Dev Back (em paralelo se não houver
   dependência).

### Etapa 3 — Devs

1. Cada Dev implementa somente a sua parcela.
2. Cada Dev roda a validação local obrigatória (ver `tarefa.md`).
3. **Gate**: validação falhou → corrigir antes de declarar pronto.
4. Declaração de conclusão por arquivo + resultado dos comandos.

### Etapa 4 — QA

1. Roda o harness completo na raiz (`harness.ps1` / `harness.sh`).
2. Confere critérios de aceite item a item e o escopo dos arquivos alterados.
3. Emite veredito:
   - **PASS** → entrega ao PO.
   - **FAIL** → relatório com evidência → dev responsável faz retrabalho →
     QA revalida (loop até PASS).

### Etapa 5 — PO (encerramento)

1. Recebe o PASS do QA.
2. Decide: aceitar a entrega e (se aplicável) atualizar documentação
   (requisitos, pendencias) e **mover o card no kanban**
   (`15-Desenvolvimento/Kanban-Desenvolvimento.kanban.md`) para o status
   correspondente.
3. Atualiza o log de handoff em `tarefa.md`.

### Etapa 6 — DOCS (sob demanda)

1. Operador pede melhoria de documentação (seção ou tema).
2. DOCS lê a seção completa, diagnostica (clareza/estrutura/links/consistência).
3. Propõe mudanças → **aprovação do operador** → aplica seção por seção.
4. QA confere links/marcadores ao final (ver `DOCS.md`).

## Modo rápido (quando NÃO usar o pipeline)

- **Pergunta informativa** (o que é X, como funciona Y, dúvida sobre uma seção
  do vault): responder direto, sem criar tarefa.
- **Pedido de documentação**: só `DOCS.md` (Etapa 6), sem PO/Tech Lead/Devs.
- **Pequeno ajuste óbvio** (typo, link quebrado, frase confusa): corrigir
  direto ou via `DOCS.md` — não gera T-xxx nem passa pelo QA.
- O pipeline é para **trabalho de entrega** (feature, refactor, integração)
  que exige código + testes + validação de critérios de aceite.

## Regras de handoff (todas as etapas)

- Cada etapa consome a saída da anterior e **não pula etapas**.
- Nada é "entregue" sem a validação da etapa seguinte.
- Evidência obrigatória: resultados de comandos, arquivos alterados, critérios.
- Nunca inventar requisitos: `[A DEFINIR]` / `[VALIDAR]` sempre do
  `14-Pendencias/Pendencias.md`.

## Mapa de validações

| Validação | Comando | Onde roda | Quando |
|-----------|---------|-----------|--------|
| Lint frontend | `npm run lint` | `frontend/` | Dev Front + harness |
| Build frontend | `npm run build` | `frontend/` | Dev Front + harness |
| Testes backend | `.\mvnw.cmd test` | `backend/` | Dev Back + harness |
| Build ingestion | `go build ./...` | `ingestion/` | Dev Back + harness |
| Testes ingestion | `go test ./...` | `ingestion/` | Dev Back + harness |
| Harness completo | `.\harness.ps1` / `./harness.sh` | raiz do repo | QA |