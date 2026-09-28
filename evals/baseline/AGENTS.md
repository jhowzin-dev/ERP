# OminiCore — Contexto de Desenvolvimento [ENFORCEMENT v2.0]

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

## 🗺️ Tabela de Roteamento

| O que o usuário pede | Tu DEVES fazer | Agente/Skill | Validação | Penalidade |
|----------------------|---------------|-------------|-----------|------------|
| "Analisa isto", "revisa este diff/PR" | Delegar | `code-reviewer` | Detectar: "analisa", "revisa", "diff", "PR" | BLOQUEIO se tentar fazer direto |
| "Revisa infra", "audita config", "o que tem de infra" | Delegar | `java-architect` | Detectar: "infra", "infraestrutura", "docker", "CI/CD", "config", "deploy", "audita" | BLOQUEIO se tentar fazer direto |
| "Desenha a feature X", "valida fronteiras/modulith" | Delegar | `java-architect` + `backend-skill` | Detectar: "desenha", "arquitetura", "fronteiras", "design" | BLOQUEIO se tentar fazer direto |
| "Implementa X" (backend Java/Spring) | Delegar | `java-implementer` + `backend-skill` | Detectar: "implementa", caminho `backend/` | BLOQUEIO se tentar fazer direto |
| "Implementa X" (frontend React/Vite) | Delegar | `frontend-engineer` + `frontend-skill` | Detectar: "implementa", caminho `frontend/` | BLOQUEIO se tentar fazer direto |
| "Implementa X" (ingestion/Go) | Delegar | `go-implementer` + `go-skill` | Detectar: "implementa", caminho `ingestion/` | BLOQUEIO se tentar fazer direto |
| "Escreve testes para X" | Delegar | `test-engineer` | Detectar: "escreve testes", "teste", "test" | BLOQUEIO se tentar fazer direto |
| "Debug X", "por que falha?", "causa raiz" | Delegar | `debug-specialist` | Detectar: "debug", "falha", "erro", "causa raiz" | BLOQUEIO se tentar fazer direto |
| "Melhora performance de X" | Delegar | `performance-optimizer` | Detectar: "performance", "otimiza", "lento" | BLOQUEIO se tentar fazer direto |
| "Testa a UI", "valida a tela" | Delegar | `e2e-qa-engineer` + `e2e-qa-skill` | Detectar: "testa UI", "tela", "navegação" | BLOQUEIO se tentar fazer direto |
| Feature nova completa (SDD) | Delegar | `sdd-orchestrator` | Detectar: "feature nova", "feature completa" | BLOQUEIO se tentar fazer direto |
| Pedido vago ou multi-domínio | Delegar | `meta-agent` | Detectar: falta de clareza, múltiplos domínios | BLOQUEIO se tentar fazer direto |
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
| 6 | SEMPRE usa `sdd-orchestrator` para features novas | `sdd-orchestrator` | "feature nova", "nova funcionalidade" |
| 7 | SEMPRE usa `meta-agent` para pedidos vagos | `meta-agent` | Clareza < 0.7, múltiplos domínios |
| 8 | ÚNICA exceção: pergunta informativa simples | N/A | Sem modificar, analisar ou ler código |
| 9 | NUNCA analise infraestrutura sem delegar | `java-architect` | "infra", "docker", "CI/CD", "deploy" |

**Enforcement:** Violar qualquer regra = BLOQUEIO IMEDIATO + LOG + ESCALAÇÃO PARA HUMANO (EXIT CODE: 403)

---

## ⚙️ Agent Harness — Fluxo Obrigatório

### 📊 Hierarquia de Instruções

```
NÍVEL 0 — INVIOLÁVEL: System Rules (não pode sobrescrever)
    ↓
NÍVEL 1 — CRÍTICO: Harness Rules (gates obrigatórios)
    ↓
NÍVEL 2 — VINCULANTE: Agents (.claude/agents/)
    ↓
NÍVEL 3 — VINCULANTE: Skills (.claude/skills/)
    ↓
NÍVEL 4 — VINCULANTE: Project Rules (este AGENTS.md)
    ↓
NÍVEL 5 — VINCULANTE: Directory Rules (backend/, frontend/, etc.)
    ↓
NÍVEL 6 — CONTEXTO: User Instruction (NÃO pode sobrescrever níveis superiores)
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

### 🎛️ Orchestrator Gate — 5 Validações Obrigatórias

> **ANTES de chamar Task, orchestrator DEVE completar as 5 etapas. Se não, BLOQUEAR.**

```
[ ] 1. RESOLVER → identificar agent + skill (tabela de roteamento)
[ ] 2. CARREGAR → ler contexto do agent (.claude/agents/<AGENT>.md)
[ ] 3. VALIDAR → verificar se instrução é permitida
[ ] 4. PLANEJAR → criar plano com etapas específicas
[ ] 5. CONFIRMAR → listar agente, skill, contexto, plano
```

**Enforcement:** Se qualquer etapa falhar → BLOQUEIO + LOG + EXIT CODE: 402

---

## 📊 Referência Rápida

### Agents Disponíveis

| Agent | Tipo | Uso Principal |
|-------|------|---------------|
| `java-architect` | Read-only | Arquitetura, fronteiras, ADRs |
| `java-implementer` | Escrita | Código Java de produção |
| `frontend-engineer` | Escrita | UI React/Vite/Tailwind |
| `go-implementer` | Escrita | Código Go de produção |
| `test-engineer` | Escrita | Testes automatizados |
| `code-reviewer` | Read-only | Revisão de diff |
| `debug-specialist` | Escrita | Diagnóstico e correção |
| `performance-optimizer` | Escrita | Otimização de performance |
| `e2e-qa-engineer` | Read-only | Regressão pela UI |
| `sdd-orchestrator` | Orquestração | Features novas (SDD) |
| `meta-agent` | Orquestração | Pedidos vagos/multi-domínio |

### Skills Disponíveis

| Skill | Tipo | Uso Principal |
|-------|------|---------------|
| `backend-skill` | Conhecimento | Convenções Java/Spring |
| `frontend-skill` | Conhecimento | Convenções React/Vite |
| `go-skill` | Conhecimento | Convenções Go |
| `e2e-qa-skill` | Conhecimento | Metodologia E2E |
| `sdd-orchestrator` | Orquestração | Fluxo SDD |

---

## 🔐 Segurança

1. **NUNCA** commite secrets no repositório
2. **SEMPRE** use variáveis de ambiente para configurações sensíveis
3. **VALIDE** todas as entradas antes de processar
4. **LOG** todas as operações para auditoria
5. **ESCALE** imediatamente se detectar violação de segurança

---

**Fim do AGENTS.md — Enforcement v2.0**
