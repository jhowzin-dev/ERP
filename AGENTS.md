# OminiCore — Contexto de Desenvolvimento

---

## OBRIGATÓRIO — Fluxo de Trabalho

> **QUALQUER modelo de IA que ler este ficheiro DEVE seguir estas regras.**
> **NÃO há exceções. NÃO há atalhos. NÃO é opcional.**

### Regra central

**NUNCA faça análise, revisão, implementação, debug ou teste de código diretamente.**
**SEMPRE delega para o agente especialista using a ferramenta Task.**

### Tabela de roteamento

| O que o usuário pede | Tu DEVES fazer | Agente/Skill |
|-------------------------|---------------|-------------|
| "Analisa isto", "revisa este diff/PR" | Delegar | `code-reviewer` |
| "Desenha a feature X", "valida fronteiras/modulith" | Delegar | `java-architect` + `backend-skill` |
| "Implementa X" (backend Java/Spring) | Delegar | `java-implementer` + `backend-skill` |
| "Implementa X" (frontend React/Vite) | Delegar | `frontend-engineer` + `frontend-skill` |
| "Escreve testes para X" | Delegar | `test-engineer` |
| "Debug X", "por que falha?", "causa raiz" | Delegar | `debug-specialist` |
| "Melhora performance de X" | Delegar | `performance-optimizer` |
| "Testa a UI", "valida a tela" | Delegar | `e2e-qa-engineer` + `e2e-qa-skill` |
| Feature nova completa (SDD) | Delegar | `sdd-orchestrator` |
| Pedido vago ou multi-domínio | Delegar | `meta-agent` |
| Pergunta informativa simples (sem tocar código) | Responder diretamente | N/A |

### Regras invioláveis

1. **NUNCA** faça análise de código sem delegar para `code-reviewer`.
2. **NUNCA** desenhe arquitetura sem delegar para `java-architect`.
3. **NUNCA** implemente código sem delegar para `java-implementer` ou `frontend-engineer`.
4. **NUNCA** diagnostique bugs sem delegar para `debug-specialist`.
5. **NUNCA** escreva testes sem delegar para `test-engineer`.
6. **SEMPRE** usa `sdd-orchestrator` para features novas.
7. **SEMPRE** usa `meta-agent` para pedidos vagos ou multi-domínio.
8. **A ÚNICA exceção** é quando o usuário faz uma pergunta informativa simples que não envolve alterar, analisar ou revisar código.

### Como delegar

Usa a ferramenta `Task` com `subagent_type` adequado. No prompt de delegação, inclui o caminho do ficheiro de agente para que o subagente leia as suas instruções:

```
Task(subagent_type="general", prompt="Leia .claude/agents/<agente>.md e execute: <tarefa>")
```

---

## Agent Harness — Fluxo Obrigatório

> **O caminho da pasta é apenas contexto de localização, não autorização para execução.**
> **Qualquer instrução que mencione um caminho de pasta DEVE passar pelo Harness antes de qualquer tool call.**

### Hierarquia de Instruções

A prioridade das instruções segue esta ordem (cada nível não pode ser sobrescrito por níveis inferiores):

```
System Rules (regras do modelo e ferramentas)
    ↓
Harness Rules (regras desta seção)
    ↓
Agents (definições em .claude/agents/)
    ↓
Skills (conhecimento em .claude/skills/)
    ↓
Project Rules (regras do projeto neste AGENTS.md)
    ↓
Directory Rules (regras específicas de pastas)
    ↓
User Instruction (pedido do usuário)
```

**Regra:** A instrução do usuário NÃO pode ignorar ou sobrescrever regras de níveis superiores.

### Execution Gate — 8 Etapas Obrigatórias

Toda operação relevante DEVE passar por este gate. Se alguma etapa obrigatória não for concluída, a execução é **bloqueada**.

```
1. Instruction
   ↓ (usuário faz pedido)
2. Resolve Agents / Skills
   ↓ (identificar quais agents e skills são necessários)
3. Load Context
   ↓ (carregar regras e contexto dos agents/skills)
4. Validate
   ↓ (validar se a instrução é permitida pelas regras superiores)
5. Plan
   ↓ (criar plano de execução com etapas)
6. Execution Gate
   ↓ (validar que todas as etapas obrigatórias foram concluídas)
7. Tool Call
   ↓ (executar ação via ferramenta)
8. Verify (Goal Gate)
   ↓ (validar resultado da execução com verificação objetiva)
```

### Goal Gate — Loop de Verificação Obligatório

> **O agente NÃO pode declarar a tarefa concluída enquanto o verificador não retornar `exit code 0`.**

O Goal Gate é a formalização da etapa 8 (Verify). Toda implementação que gere código executável DEVE passar pelo Goal-Based Loop antes de entregar resultado.

#### Ciclo obrigatório

```
Implementação concluída
    ↓
1. Executar comandos de verificação (por domínio)
    ↓
2. Exit code 0? ──SIM──→ GOAL REACHED ✓ (tarefa concluída)
    │
    NÃO
    ↓
3. Capturar exit code + logs completos
    ↓
4. Analisar causa raiz (máx 30s)
    ↓
5. Corrigir código respeitando regras e convenções
    ↓
6. Re-executar comandos de verificação
    ↓
7. Tentativa < 5? ──SIM──→ Volta ao passo 2
    │
    NÃO (limite atingido)
    ↓
8. GOAL NOT REACHED → Output com motivo + logs → Escalonar para humano
```

#### Comandos de verificação por domínio

| Domínio | Comando | Timeout |
|---------|---------|---------|
| `backend/` | `.\mvnw.cmd test` (Windows) / `./mvnw test` (Linux) | 180s |
| `frontend/` | `npm run lint` + `npm run build` | 60s |
| `ingestion/` | `go build ./...` + `go test ./...` | 60s |

#### Safety Rails

| Regra | Valor |
|-------|-------|
| Máximo de tentativas | 5 por ciclo de verificação |
| Timeout por execução | 180s (backend) / 60s (frontend/ingestion) |
| Preservar logs | Última falha sempre no output |
| Interromper no limite | Após tentativa 5, NÃO tentar novamente |
| Re-delegação | Máximo 1 re-delegação automática com contexto do erro |

#### Output obrigatório do agente

Todo agente implementer DEVE incluir no resultado final:

```
Status: GOAL REACHED | GOAL NOT REACHED
Tentativas: N/5
[Se GOAL NOT REACHED]:
  - Motivo: <descrição do problema>
  - Logs: <último erro completo>
  - Ação recomendada: <correção necessária ou escalonamento>
```

#### Re-delegação automática (Orchestrator)

Quando o output do subagente contiver `GOAL NOT REACHED`:

1. **Primeira ocorrência:** Re-delegar para o mesmo agent com contexto do erro (prompt inclui motivo + logs).
2. **Segunda ocorrência (ou persistência):** Escalonar para o humano com relatório completo.

#### Integração com agents

| Agent | Goal Gate aplicável? | Comportamento |
|-------|---------------------|---------------|
| `java-implementer` | Sim | Loop com `.\mvnw.cmd test` (timeout 180s) |
| `go-implementer` | Sim | Loop com `go build` + `go test` (timeout 60s) |
| `frontend-engineer` | Sim | Loop com `npm run lint` + `npm run build` (timeout 60s) |
| `test-engineer` | Sim | Loop com comandos de teste do módulo (timeout conforme domínio) |
| `debug-specialist` | Sim | Loop com comandos de teste que validam o fix (timeout conforme domínio) |
| `performance-optimizer` | Sim | Loop com comandos de teste + comparação de métrica (timeout conforme domínio) |
| `code-reviewer` | Não | Read-only — validação por checklist |
| `java-architect` | Não | Read-only — validação por checklist |
| `e2e-qa-engineer` | Não | UI-based — validação por cenário |

### Orchestrator Gate — Fluxo Obligatório antes de Delegar

> **ANTES de chamar a ferramenta Task, o orchestrator DEVE completar as 5 etapas abaixo.**
> **Se qualquer etapa não for concluída, a delegação é BLOQUEADA.**

#### Checklist obrigatório (orchestrator)

```
ANTES de delegar, o orchestrator DEVE:

[ ] 1. RESOLVER: Identificar agent + skill (usar tabela de roteamento)
[ ] 2. CARREGAR: Ler contexto obrigatório do agent (## Contexto obrigatório)
[ ] 3. VALIDAR: Verificar se instrução é permitida (regras superiores)
[ ] 4. PLANEJAR: Criar plano com etapas específicas da tarefa
[ ] 5. CONFIRMAR: Listar agent, skill e plano antes de chamar Task

Se qualquer item não for concluído → BLOQUEAR delegação.
```

#### Template de delegação obrigatório

Todo Task call DEVE seguir este formato:

```
Task(
  subagent_type="general",
  prompt="Leia .claude/agents/<AGENT>.md e execute:
  
  CONTEXTO:
  - Skill: <SKILL>
  - Plano: <ETAPAS DO PLANO>
  - Timeout: <TIMEOUT DO DOMÍNIO>
  
  TAREFA:
  <DESCRIÇÃO ESPECÍFICA>
  
  VALIDAÇÃO:
  <COMANDOS DE VERIFICAÇÃO>
  
  OUTPUT ESPERADO:
  Status: GOAL REACHED | GOAL NOT REACHED
  Tentativas: N/5"
)
```

#### Validação pós-delegação

Após o agent retornar resultado, o orchestrator DEVE:

1. Verificar se output contém `GOAL REACHED` ou `GOAL NOT REACHED`
2. Se `GOAL NOT REACHED` → re-delegar com contexto do erro (máx 1x)
3. Se persistir → escalonar para humano
4. **NÃO** declarar tarefa concluída sem confirmar `GOAL REACHED`

#### Exceções

| Cenário | Permite pular Orchestrator Gate? |
|---------|--------------------------------|
| Pergunta informativa simples (sem tocar código) | Sim — única exceção |
| Leitura direta de arquivo (sem modificação) | Sim — após validar que é leitura |
| Qualquer operação de escrita/implementation | **NÃO** — Gate obrigatório |
| Auditoria/analysis de código | **NÃO** — Gate obrigatório |

### Regras de Bloqueio

| Cenário | Ação |
|---------|------|
| Instrução menciona caminho de pasta | BLOQUEAR até passar pelo Harness completo |
| Caminho aponta para `backend/` | Resolver `java-architect` ou `java-implementer` + `backend-skill` |
| Caminho aponta para `frontend/` | Resolver `frontend-engineer` + `frontend-skill` |
| Caminho aponta para `ingestion/` | Resolver `go-implementer` + `go-skill` |
| Caminho aponta para `.claude/agents/` ou `.claude/skills/` | Apenas leitura, sem modificação sem aprovação |
| Etapa obrigatória não concluída | BLOQUEAR execução |
| Pergunta informativa simples (sem tocar código) | ÚNICA exceção — responder diretamente |

### Tabela de Decisão com Detecção de Caminho

| O que o usuário pede | Caminho detectado? | Tu DEVES fazer | Agente/Skill |
|-------------------------|-------------------|---------------|-------------|
| "Analisa isto", "revisa este diff/PR" | Sim/Não | Delegar | `code-reviewer` |
| "Desenha a feature X" | Não | Delegar | `java-architect` + `backend-skill` |
| "Implementa X" (backend) | `backend/...` | Delegar | `java-implementer` + `backend-skill` |
| "Implementa X" (frontend) | `frontend/...` | Delegar | `frontend-engineer` + `frontend-skill` |
| "Escreve testes para X" | Sim/Não | Delegar | `test-engineer` |
| "Debug X" | Sim/Não | Delegar | `debug-specialist` |
| "Melhora performance de X" | Sim/Não | Delegar | `performance-optimizer` |
| "Testa a UI" | Sim/Não | Delegar | `e2e-qa-engineer` + `e2e-qa-skill` |
| Feature nova completa | Não | Delegar | `sdd-orchestrator` |
| Pedido vago ou multi-domínio | Sim/Não | Delegar | `meta-agent` |
| "Leia o arquivo X" (leitura) | Sim | Ler diretamente (após validar) | N/A |
| "Modifique X" (escrita) | Sim | BLOQUEAR → Delegar | Agent correspondente |
| Pergunta informativa simples | Qualquer | Responder diretamente | N/A |

### Validação por Caminho

Quando um caminho é detectado na instrução, execute as seguintes validações:

1. **Identificar domínio:** `backend/`, `frontend/`, `ingestion/`, `.claude/`, `docs/`, etc.
2. **Resolver agent:** Usar tabela de roteamento para identificar o agent correto
3. **Resolver skill:** Identificar skill de conhecimento necessária
4. **Validar permissão:** Verificar se o agent tem permissão para o tipo de operação (leitura/escrita)
5. **Carregar contexto:** O agent deve ler a skill correspondente antes de executar
6. **Criar plano:** Definir etapas específicas da operação
7. **Gate de execução:** Validar que todas as etapas anteriores foram concluídas
8. **Executar:** Apenas após todas as validações
9. **Verificar resultado:** Validar se a execução foi bem-sucedida

---

## Monorepo

| Pasta | Tecnologia |
|-------|-----------|
| `backend/` | Java 21, Spring Boot 4.0.7, Spring Modulith (Maven) |
| `frontend/` | React 19, Vite 8, Tailwind v4, TypeScript strict |
| `ingestion/` | Go 1.22, kafka-go (webhooks ML, sync estoque/preço) |

Mapa completo de pastas e comandos de build: [`docs/README.md`](docs/README.md)

## Fonte principal - SDD

- **Especificação do produto:** [`docs/sdd/OMINICORE-SDD.md`](docs/sdd/OMINICORE-SDD.md) - princípios, camadas, fases A–E, gates de verificação.
- **Fluxo por feature:** [`docs/sdd/SDD-ORCHESTRATOR.md`](docs/sdd/SDD-ORCHESTRATOR.md) e [`docs/sdd/SDD-USAGE-GUIDE.md`](docs/sdd/SDD-USAGE-GUIDE.md). Artefactos em `docs/features/<feature-id>/`.
- **ADRs:** [`docs/sdd/adrs/`](docs/sdd/adrs/) - decisões estruturais duradouras.

## Agentes especialistas (`.claude/agents/`)

Invoca pelo **nome** com a ferramenta Agent. Cada agente já traz a sua allowlist de
ferramentas e lê a skill correspondente no arranque — não copies convenções para o prompt de delegação.
Índice e padrão de escrita: [`docs/agents/README.md`](docs/agents/README.md).

| Situação | Agente |
|----------|--------|
| Fronteiras / layering / API shape (read-only) | `java-architect` |
| Implementação Java/Spring concreta | `java-implementer` |
| Implementação Go (ingestion, workers, Kafka) | `go-implementer` |
| UI / React / Vite / Tailwind | `frontend-engineer` |
| Testes automatizados | `test-engineer` |
| Qualidade de PR / diff (read-only) | `code-reviewer` |
| Bugs / causa raiz | `debug-specialist` |
| Performance com evidência | `performance-optimizer` |
| QA End-to-End (navega a UI real) | `e2e-qa-engineer` |

Orquestração mínima: um especialista quando bastar; cadeias curtas só quando a tarefa exigir.

## Skills (`.claude/skills/`)

Carregadas automaticamente quando a situação encaixa. Índice e padrão:
[`docs/skills/README.md`](docs/skills/README.md).

| Área | Skill |
|------|-------|
| Convenções backend Java/Spring (conhecimento) | `backend-skill` |
| Convenções frontend React/Vite/Tailwind (conhecimento) | `frontend-skill` |
| Convenções Go/ingestion (conhecimento) | `go-skill` |
| Pedido vago ou multi-domínio → rotear e encadear | `meta-agent` |
| Especificar feature antes de código (gate por fase) | `sdd-orchestrator` |
| Regressão E2E pela UI real | `e2e-qa-skill` |

Orquestração é skill, não agente: um subagente não tem a ferramenta Agent e por isso só conseguiria
recomendar, não delegar.

## Regras de comportamento

- **SDD first:** para features novas ou refactors com contrato negócio/técnico, seguir o fluxo SDD (PRD → design → spec/tasks) antes de gerar código.
- **Human-in-the-loop:** merge e decisões de risco ficam com o humano. Sem secrets no repo.
- **Segurança:** autorização (RBAC) explícita onde o SDD e a feature exigirem; validar inputs na fronteira.
- **Modulith:** dependências entre módulos de negócio apenas via eventos Kafka ou injeção controlada. **Não** criar dependências diretas entre módulos diferentes.
- **Frontend:** TypeScript `strict`, sem `any`, Tailwind v4 — não expandir para outro CSS framework.
- **Idioma:** respostas e artefactos em **português (Brasil)**; identificadores de código em inglês.
