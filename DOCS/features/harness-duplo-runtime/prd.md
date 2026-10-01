---
version: 1
status: draft
---

# PRD — Harness OpenCode Universal

## 1. Problema
O harness OminiCore está com nota 5.4/10. O desenho de papéis está acima da média, mas o loop de evals e a governança prática estão partidos. Governança “por design” existe no papel; no runtime OpenCode quase nada é aplicado.
Riscos identificados: duplo AGENTS.md sempre-on, paths mortos para `.claude/`, evals sem `evals.json` e com heurística 60% de keywords, skills com orquestração misturada, `frontend-design` inexistente, `AGENTS.md` longo e duplicado.

## 2. Personas
- **Tech Lead / Orchestrator**: precisa de roteamento confiável, gates verificáveis e delegação sem edição de código produto.
- **Developer**: quer instruções de skill precisas, sem paths mortos, e validação automática via Goal Gate.
- **QA / Harness Owner**: precisa de evals executáveis que meçam roteamento, não-regressão de path e Goal Gate.

## 3. Funcionalidades

1. **Fonte única de verdade**
   - Apenas `.opencode/agents` e `.opencode/skills` são fonte.
   - OpenCode consome diretamente, sem duplicação de conteúdo.
   - Critério de aceite: `grep -r "\.claude/" .opencode` retorna 0 resultados.

2. **AGENTS.md curto e sempre-on**
   - ~80-120 linhas: hierarquia, tabela de roteamento, proibições, Goal Gate com comandos.
   - Sem códigos HTTP fictícios e sem duplicação de baseline.
   - Critério de aceite: tamanho <150 linhas e contém apenas referência para agent files.

3. **Baseline fora do always-on**
   - Renomear `evals/baseline/AGENTS.md` para `AGENTS.baseline.md`.
   - Garantir apenas um AGENTS.md sempre-on.
   - Critério de aceite: `AGENTS.md` único na raiz, baseline não injectado.

4. **Paths consistentes**
   - Substituir todas refs `.claude/` → `.opencode/` em agents, skills, DOCS/.
   - Remover leftovers: DbContext, AsNoTracking, xUnit/Cucumber, impeccable-harness cru.
   - Incluir ingestion/ em debug/test/performance.
   - Critério de aceite: Read de skill resolve em `.opencode/skills/.../SKILL.md`.

5. **Evals executáveis**
   - Criar `evals/evals.json` com 12-20 casos cobrindo roteamento, não-regressão de path, Goal Gate.
   - Corrigir runner: caminho `evals/evals.json` (não `evals/evals/evals.json`).
   - Substituir heurística 60% por asserts estruturados: expect_agent, expect_no_edit, expect_files, expect_exit_0.
   - Critério de aceite: `python evals/scripts/run_eval.py --dir .` executa ≥12 casos e gera `evals/results.json`.

6. **Runner universal**
   - OpenCode: manter `opencode.json`; instruções encurtadas para AGENTS.md apenas.
   - Evals funcionam com qualquer modelo LLM via OpenCode, sem dependência de runtime específico.
   - Critério de aceite: `python evals/scripts/run_eval.py --dir .` executa com modelos NVIDIA/OpenCode.

7. **Skills e agents limpos**
   - `frontend-design` ou criar skill mínima ou remover da tabela.
   - Descrições de trigger curtas em YAML; corpo com factos de repo.
   - `meta-agent` e `sdd-orchestrator` sem duplicar AGENTS.md.
   - Critério de aceite: zero referências `.claude/` no harness ativo.

## 4. Métricas de sucesso
- Nota subjectiva do harness ≥8.0.
- `evals/results.json` com pass rate ≥80% após baseline corrigida.
- AGENTS.md <150 linhas.
- Zero referências `.claude/` em `.opencode/`.
- Tempo always-on reduzido (tokens sempre-on descem).

## 5. Fora de escopo
- Refatorar código produto backend/frontend/ingestion.
- Alterar lógica de negócio.
- Criar novos agentes de produto.

## 6. Pendências
- [VALIDAR] Layout exato de `evals/` existente no repo.
