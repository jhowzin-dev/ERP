# Template de Tarefa (Handoff PO → Tech Lead → Devs)

> Preenchido pelo PO. Nenhum campo obrigatório pode ficar vazio antes da
> delegação. Copie este arquivo por tarefa (ex.: `tarefa-RF003.md`) ou
> preencha inline no handoff.

---

## ID da tarefa

`T-<número>` (incremental) — vincular à RF/RN quando existir: `RF-xx / RN-xx`

## Card do kanban

> Nome do card em `15-Desenvolvimento/Kanban-Desenvolvimento.kanban.md` que esta
> tarefa move (ex.: "Backend: RF-xxx"). O PO atualiza o status ao aceitar.

## Contexto / motivação

> Por que essa tarefa existe? Qual problema resolve? (1-3 frases)

## Regras de negócio aplicáveis

- [ ] RN-xx — descrição (referência: `07-Regras-Negocio/Regras-Negocio.md`)
- [ ] Nenhuma RN nova identificada — sinalizar `[VALIDAR]` se o pedido implica regra nova

## Módulos afetados

> Lista da `04-Modulos/Modulos.md`.

## Divisão front/back

| Camada | Entrega esperada | Arquivos-alvo (Tech Lead preenche) |
|--------|------------------|-------------------------------------|
| Frontend | O que o usuário vê/interage | |
| Backend | API, regras, persistência | |
| Ingestão (Go) | ETL/webhooks, se aplicável | |

## Contrato de dados (Tech Lead preenche)

> DTOs, endpoints, payloads, props — definido ANTES da implementação.

## Critérios de aceite

> Da `12-Criterios-Aceitacao/Criterios-Aceitacao.md` quando existir, senão
> definidos aqui pelo PO (testáveis, um por linha):

- [ ] 
- [ ] 

## Validação exigida (harness — fonte única)

- [ ] Frontend: `.\harness.ps1 frontend` (lint + build)
- [ ] Backend: `.\harness.ps1 backend` (exige `docker compose up -d` em `infra/`)
- [ ] Ingestão: `.\harness.ps1 ingestion` (exige Go instalado)

## Pendências

- [ ] `[A DEFINIR]` — bloqueia a tarefa até decisão
- [ ] `[VALIDAR]` — risco, confirmar antes de prosseguir

## Log de handoff

| Etapa | Agente | Data | Observação |
|-------|--------|------|------------|
| Criação | PO | | |
| Plano técnico | Tech Lead | | |
| Implementação | Dev Front / Dev Back | | |
| Validação | QA | | PASS / FAIL |