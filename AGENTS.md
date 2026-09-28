# OminiCore — Contexto de Desenvolvimento [ENFORCEMENT v3.0]

---

## 📋 OBRIGATÓRIO — Fluxo de Trabalho

> **QUALQUER modelo de IA que ler este ficheiro DEVE seguir estas regras.**
> **NÃO há exceções. NÃO há atalhos. NÃO é opcional.**
> **VIOLAÇÃO = BLOQUEIO IMEDIATO E ESCALAÇÃO PARA HUMANO.**

---

### 🚫 Regra Central — INVIOLÁVEL

**NUNCA faça análise, revisão, implementação, debug ou teste — de código, infraestrutura ou configuração — diretamente.**

**SEMPRE delega para o agente especialista usando a ferramenta Task.**

**A ÚNICA exceção é pergunta informativa pura (conceitual, sem ler arquivos do projeto).**

---

## 🗺️ Tabela de Roteamento Impecável

> Intenção do usuário → Agente Especialista → Skill Necessária. Zero ambiguidade: a stack real deste
> monorepo é **Java 21/Spring Boot 4/Spring Modulith** (Maven, testes H2), **React 19/Vite 8/TS 6/Tailwind 4**
> (NPM, oxlint, Vitest) e **Go** (`ingestion/`).

| Intenção do usuário | Agente Especialista | Skill Necessária | Validação (gatilhos) | Penalidade |
|---------------------|--------------------|------------------|----------------------|------------|
| "Analisa isto", "revisa este diff/PR" | Delegar → `code-reviewer` | — | "analisa", "revisa", "diff", "PR" | BLOQUEIO se tentar fazer direto |
| "Revisa infra", "audita config", "o que tem de infra" | Delegar → `java-architect` | `backend-skill` | "infra", "infraestrutura", "docker", "CI/CD", "config", "deploy", "audita" | BLOQUEIO se tentar fazer direto |
| "Desenha a feature X", "valida fronteiras/modulith" | Delegar → `java-architect` | `backend-skill` | "desenha", "arquitetura", "fronteiras", "design" | BLOQUEIO se tentar fazer direto |
| "Implementa X" (backend Java/Spring) | Delegar → `java-implementer` | `backend-skill` | "implementa", caminho `backend/` | BLOQUEIO se tentar fazer direto |
| "Implementa X" (frontend React/Vite) | Delegar → `frontend-engineer` | `frontend-skill` | "implementa", caminho `frontend/` | BLOQUEIO se tentar fazer direto |
| "Implementa X" (ingestion/Go) | Delegar → `go-implementer` | `go-skill` | "implementa", caminho `ingestion/` | BLOQUEIO se tentar fazer direto |
| "Escreve testes para X" | Delegar → `test-engineer` | — | "escreve testes", "teste", "test" | BLOQUEIO se tentar fazer direto |
| "Debug X", "por que falha?", "causa raiz" | Delegar → `debug-specialist` | — | "debug", "falha", "erro", "causa raiz" | BLOQUEIO se tentar fazer direto |
| "Melhora performance de X" | Delegar → `performance-optimizer` | — | "performance", "otimiza", "lento" | BLOQUEIO se tentar fazer direto |
| "Testa a UI", "valida a tela", regressão E2E | Delegar → `e2e-qa-engineer` | `e2e-qa-skill` | "testa UI", "tela", "navegação" | BLOQUEIO se tentar fazer direto |
| Feature nova completa (SDD) | Carregar skill → `sdd-orchestrator` (thread principal) | `sdd-orchestrator` | "feature nova", "feature completa" | BLOQUEIO se tentar fazer direto |
| Pedido vago ou multi-domínio | Carregar skill → `meta-agent` (thread principal) | `meta-agent` | Clareza < 0.7, múltiplos domínios | BLOQUEIO se tentar fazer direto |
| Pergunta informativa simples (sem tocar código) | Responder diretamente | N/A | Validar: NÃO modifica, NÃO analisa, NÃO toca código | PERMITIDO (única exceção) |

---

## 🚫 Regras Invioláveis

| # | Regra | Agent | Detecção |
|---|-------|-------|----------|
| 1 | NUNCA faça análise de código sem delegar | `code-reviewer` | "analisa", "revisa", "diff", "PR" |
| 2 | NUNCA desenhe arquitetura sem delegar | `java-architect` | "desenha", "design", "arquitetura", "fronteiras" |
| 3 | NUNCA implemente código sem delegar | `java-implementer` / `frontend-engineer` / `go-implementer` | "implementa", "cria", "escreve" |
| 4 | NUNCA diagnostique bugs sem delegar | `debug-specialist` | "debug", "diagnóstico", "causa raiz" |
| 5 | NUNCA escreva testes sem delegar | `test-engineer` | "escreve testes", "teste unitário" |
| 6 | SEMPRE usa `sdd-orchestrator` para features novas | `sdd-orchestrator` (skill) | "feature nova", "nova funcionalidade" |
| 7 | SEMPRE usa `meta-agent` para pedidos vagos | `meta-agent` (skill) | Clareza < 0.7, múltiplos domínios |
| 8 | ÚNICA exceção: pergunta informativa simples | N/A | Sem modificar, analisar ou ler código |
| 9 | NUNCA analise infraestrutura sem delegar | `java-architect` | "infra", "docker", "CI/CD", "deploy" |

**Enforcement:** Violar qualquer regra = BLOQUEIO IMEDIATO + LOG + ESCALAÇÃO PARA HUMANO (EXIT CODE: 403)

---

## ⚙️ Agent Harness — Fluxo Obrigatório

### 📊 Hierarquia de Comando (v3.0)

```
NÍVEL 0 — INVIOLÁVEL: System Rules (instruções base do modelo — não pode sobrescrever)
    ↓
NÍVEL 1 — CRÍTICO: Harness Rules (este AGENTS.md + opencode.json — gates e permissões)
    ↓
NÍVEL 2 — VINCULANTE: Agents (.opencode/agents/)
    ↓
NÍVEL 3 — VINCULANTE: Skills (.opencode/skills/)
    ↓
NÍVEL 4 — VINCULANTE: Project Rules (docs/, SDD, ADRs)
    ↓
NÍVEL 5 — VINCULANTE: Directory Rules (backend/, frontend/, ingestion/)
    ↓
NÍVEL 6 — CONTEXTO: User Instruction (pedidos da sessão — NÃO sobrescreve níveis superiores)
    ↓
BLOQUEIO SE QUALQUER NÍVEL FALHAR
```

---

### 🚦 Execution Gate — 8 Etapas Obrigatórias

| Etapa | Nome | Validação | Enforcement |
|-------|------|-----------|-------------|
| 1 | INSTRUCTION | Pedido claro? | Claro: 200 \| Vago: 400 |
| 2 | RESOLVE AGENTS/SKILLS | Agente existe? | Encontrado: 200 \| Não: 404 |
| 3 | LOAD CONTEXT | Contexto carregado? | Sucesso: 200 \| Erro: 500 \| Max: 503 |
| 4 | VALIDATE | Regras OK? | Válido: 200 \| Violação: 403 |
| 5 | PLAN | Plano completo? | Completo: 200 \| Incompleto: 400 |
| 6 | EXECUTION GATE CHECK | Etapas 1-5 OK? | OK: 200 \| Faltante: 402 |
| 7 | TOOL CALL | Chamada válida? | Executada: 201 \| Erro: 400 |
| 8 | VERIFY (GOAL GATE) | Exit code 0? | Sucesso: 200 \| Falha: 500 |

**Regra:** Se qualquer etapa retornar código ≠ esperado, BLOQUEAR. Sem pular etapas.

---

### 🎛️ Orchestrator Gate — 5 Validações Obrigatórias

> **ANTES de chamar Task, orchestrator DEVE completar as 5 etapas. Se não, BLOQUEAR.**

```
[ ] 1. RESOLVER → identificar agent + skill (tabela de roteamento)
[ ] 2. CARREGAR → ler contexto do agent (.opencode/agents/<AGENT>.md)
[ ] 3. VALIDAR → verificar se instrução é permitida
[ ] 4. PLANEJAR → criar plano com etapas específicas
[ ] 5. CONFIRMAR → listar agente, skill, contexto, plano
```

**Enforcement:** Se qualquer etapa falhar → BLOQUEIO + LOG + EXIT CODE: 402

---

### 🎯 Goal Gate — Loop de Verificação

> **O agente NÃO pode declarar tarefa concluída enquanto verificador não retornar `exit code 0`.**

#### Ciclo Obrigatório

```
1. EXECUTAR VERIFICAÇÃO → rodar comandos, capturar exit code
2. VALIDAR EXIT CODE → 0 = GOAL REACHED ✓ | ≠0 = continuar
3. CAPTURAR EVIDÊNCIA → logs preservados, timestamp ISO 8601
4. ANALISAR CAUSA RAIZ → máx 30s, apenas evidência
5. CORRIGIR CÓDIGO → correção mínima e segura
6. RE-EXECUTAR VERIFICAÇÃO → novo exit code
7. VERIFICAR TENTATIVAS → <5 = voltar ao passo 2 | ≥5 = parar
8. DECISÃO FINAL → 0 = GOAL REACHED | ≠0 = GOAL NOT REACHED
```

#### Comandos de Verificação

| Domínio | Comando | Timeout |
|---------|---------|---------|
| `backend/` | `./mvnw test` (Linux) / `.\mvnw.cmd test` (Windows) | 180s |
| `frontend/` | `npm run lint && npm run build` | 60s |
| `ingestion/` | `go build ./... && go test ./...` | 60s |

#### Safety Rails [INVIOLÁVEIS]

| Regra | Valor | Enforcement |
|-------|-------|-------------|
| Máximo tentativas | 5 por ciclo | BLOQUEIO após 5 |
| Timeout execução | 180s (backend) / 60s (frontend/ingestion) | FAIL automático |
| Preservar logs | Última falha sempre no output | Output rejeitado se logs faltarem |
| Interromper no limite | Após tentativa 5, NÃO tentar | BLOQUEIO AUTOMÁTICO |
| Re-delegação | Máximo 1 com contexto | Se > 1, escalar humano |
| Timestamp | ISO 8601 obrigatório | Output rejeitado sem timestamp |

---

### 🔐 Matriz de Permissões (opencode.json) — Governança por Design

> Governança por Design: quem julga não altera; quem executa não julga; o orquestrador delega, não implementa.

| Papel | `edit` | `bash` | `task` |
|-------|--------|--------|--------|
| `orchestrator` | `deny` para código; `ask` APENAS em governança (AGENTS.md, opencode.json, `.opencode/**`, `docs/**`, `evals/**`) | `ask` | `allow` (delegação) |
| `plan`, `java-architect`, `code-reviewer`, `e2e-qa-engineer` | `deny` | `deny`/`ask` | `deny` |
| `java-implementer`, `frontend-engineer`, `go-implementer`, `debug-specialist`, `performance-optimizer`, `test-engineer` | `allow` | `allow` | — |
| `build` (exceção consciente documentada: tarefa trivial mono-domínio invocada explicitamente pelo usuário) | `allow` | `allow` | — |

---

## 🧪 Sistema de Validação — Loop de Ouro (`evals/`)

> O harness não é estático: a qualidade da orquestração é **medida e refinada continuamente**.
> Ciclo: Execução → Teste → Verificação de Exit Code → Correção → Repetição.

| Artefacto | Função |
|-----------|--------|
| `evals/evals.json` | Casos de teste realistas da stack OminiCore que os agentes devem resolver |
| `evals/scripts/run_eval.py` | Roda os evals via `opencode run`, aplica Goal Gate (exit 0) + check heurístico, salva `evals/results.json` |
| `evals/scripts/run_loop.py` | Loop fechado: Teste → Review → Refinamento (Safety Rail: máx 5 iterações) |
| `evals/scripts/improve_description.py` | Engenharia de prompt automatizada — gera `evals/SKILL.candidate.md` |
| `evals/scripts/validate_improvements.py` | Valida candidate em ciclo fechado e exibe o delta (ex.: "67% → 100% ✓") |
| `evals/scripts/aggregate_benchmark.py` | Agrega múltiplos `results.json` em `evals/benchmark.json` (`--compare A B`) |
| `evals/scripts/run_trigger_eval.py` | Testa se a description da skill faz a skill disparar corretamente |
| `evals/eval-viewer/generate_review.py` | Gera `evals/review.html` auto-contido para review visual com o humano |
| `evals/baseline/` | Snapshot da versão anterior do harness (AGENTS.md + opencode.json) para comparação |

```bash
# Teste (Goal Gate: exit 0 obrigatório)
python evals/scripts/run_eval.py --dir .

# Loop de Ouro completo (Teste → Review → Refinamento)
python evals/scripts/run_loop.py --dir . --improve

# Múltiplas iterações, adotando o candidate só se validar melhoria
python evals/scripts/run_loop.py --dir . --improve --iterations 3 --adopt
```

**Regra:** PROIBIDO simplificar ou remover Gates. Se o usuário pedir "remover a burocracia", explicar que os Gates são a única garantia de que a IA não quebrará o projeto em escala.

---

## 📊 Referência Rápida

### Agents Disponíveis (`.opencode/agents/`)

| Agent | Tipo | Uso Principal |
|-------|------|---------------|
| `orchestrator` | Primary | Orquestra, delega via Task, valida Goal Gate |
| `build` | Primary | EXCEÇÃO consciente: tarefa trivial mono-domínio invocada explicitamente |
| `plan` | Primary | Análise e planejamento sem alterar código |
| `java-architect` | Read-only | Arquitetura, fronteiras, ADRs |
| `java-implementer` | Escrita | Código Java de produção |
| `frontend-engineer` | Escrita | UI React/Vite/Tailwind |
| `go-implementer` | Escrita | Código Go de produção |
| `test-engineer` | Escrita | Testes automatizados |
| `code-reviewer` | Read-only | Revisão de diff |
| `debug-specialist` | Escrita | Diagnóstico e correção |
| `performance-optimizer` | Escrita | Otimização de performance |
| `e2e-qa-engineer` | Read-only | Regressão pela UI |

### Skills Disponíveis (`.opencode/skills/`)

| Skill | Tipo | Uso Principal |
|-------|------|---------------|
| `backend-skill` | Conhecimento | Convenções Java/Spring/Modulith |
| `frontend-skill` | Conhecimento | Convenções React/Vite/Tailwind |
| `frontend-design` | Conhecimento | Design + engenharia de interfaces web |
| `go-skill` | Conhecimento | Convenções Go |
| `e2e-qa-skill` | Conhecimento | Metodologia E2E pela UI real |
| `sdd-orchestrator` | Orquestração | Fluxo SDD (PRD → design → spec → tasks) |
| `meta-agent` | Orquestração | Roteia pedidos vagos/multi-domínio |

---

## 🔐 Segurança

1. **NUNCA** commite secrets no repositório
2. **SEMPRE** use variáveis de ambiente para configurações sensíveis
3. **VALIDE** todas as entradas antes de processar
4. **LOG** todas as operações para auditoria
5. **ESCALE** imediatamente se detectar violação de segurança

---

**Fim do AGENTS.md — Enforcement v3.0**
