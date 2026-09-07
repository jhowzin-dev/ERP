---
name: e2e-qa-skill
description: Executa uma regressão End-to-End exploratória do frontend do OminiCore pela UI real (Browser pane), delegando a execução ao subagent e2e-qa-engineer módulo a módulo e consolidando um relatório versionado. Contém a metodologia canónica — pré-condições de ambiente, matriz de cenários, priorização, escala de severidade e templates de defeito e de relatório. Use quando o utilizador pedir para "testar o frontend", "rodar regressão", "fazer QA de X", "validar essa tela antes de mergear" ou reproduzir um bug relatado, e depois de alterar algo em frontend/src. Não use para testes Cucumber (é código — test-engineer) nem para revisão estática de diff (code-reviewer).
---

# Regressão E2E — OminiCore (frontend)

Fonte **única** da metodologia E2E e da sua orquestração. Testa a aplicação **como um utilizador real**,
através da interface visual — não pela leitura de código. Complementa, não substitui, os cenários de teste
existentes ([`frontend-skill`](../frontend-skill/SKILL.md) §10).

**Execução:** esta skill corre na thread principal e delega ao subagent
[`e2e-qa-engineer`](../../agents/e2e-qa-engineer.md), que detém as ferramentas de Browser.
Esse agent lê este ficheiro no arranque — não repetir a metodologia dentro do prompt de delegação.

Argumento opcional de escopo: `catalog`, `inventory`, `sales`, `finance`, `customers`, `dashboard`, `marketplace`.
Vazio = regressão completa.

---

## 1. Quando aplicar

| Situação | Aplicar |
| -------- | ------- |
| Regressão completa antes de release | Sim |
| Validar uma feature nova ponta-a-ponta (acesso → operação → confirmação) | Sim |
| Reproduzir um bug relatado, navegando o fluxo real | Sim |
| Auditoria de UX: consistência visual, estados, responsividade | Sim |
| Escrever/correr teste unitário, integração ou Cucumber | Não — agent `test-engineer` |
| Revisar apenas um diff/PR | Não — agent `code-reviewer` |
| Diagnosticar a causa raiz de um bug já reproduzido | Não — agent `debug-specialist` |

---

## 2. Passo 0 — Pré-condições (sempre primeiro, e bloqueantes)

| Serviço | Como subir | Porta |
| ------- | ---------- | ----- |
| Frontend | `npm run dev` em `frontend/` | `5173` |
| API (Spring Boot) | `./mvnw spring-boot:run` em `backend/` | `8080` |
| Banco (PostgreSQL) | `docker compose up -d` em `infra/` | `5432` |

1. **Ambiente de pé.** Confirmar que frontend, backend e banco estão rodando.
2. **Confirmar que é o app certo.** Ler o título/conteúdo da página ("OminiCore"). Se for outra coisa, pode ser outro projecto local na mesma porta — **parar e avisar**.
3. **Confirmar a API acessível** antes de qualquer fluxo autenticado ou com dado real. Se não estiver, **parar e registar bloqueio de ambiente** — testar o frontend contra uma API fora do ar produz falsos positivos e negativos.
4. **Confirmar restrições de dados** com o utilizador antes de iniciar CRUDs (ex.: "não criar produtos novos", "não mexer nos pedidos existentes").

Qualquer pré-condição falhada interrompe a execução e vira item de **Riscos** no relatório (§8). Nunca prosseguir assumindo comportamento.

---

## 3. Fase 1 — Mapeamento

Percorrer a árvore real de rotas (`frontend/src/pages/`) e listar módulos + fluxos críticos.
Ponto de partida conhecido — **confirmar, o mapa evolui**:

| Grupo | Rotas | Natureza |
| ----- | ----- | -------- |
| Públicas | `/login`, `/register` | Público, sem sessão |
| Catálogo | `/catalog/produtos`, `/catalog/produtos/:id` | Público ou autenticado, listagem + detalhe |
| Autenticadas | `/dashboard`, `/inventory/estoque`, `/sales/pedidos`, `/finance/relatorios`, `/customers` | Autenticado, RBAC por papel |
| Marketplace | `/marketplace/integrations` | Autenticado, integração externa |

Para cada rota, identificar: exige autenticação? exige papel específico? é CRUD? tem formulário? tem filtro/busca/paginação?

---

## 4. Fase 2 — Matriz de cenários

Campos mínimos por cenário:

| Campo | Descrição |
| ----- | --------- |
| ID | `E2E-<módulo>-<sequencial>` (ex.: `E2E-CATALOG-003`) |
| Módulo | Feature/rota |
| Cenário | Frase curta do que é testado |
| Tipo | Positivo / Negativo / Extremo |
| Prioridade | Crítica / Alta / Média / Baixa (§5) |
| Pré-condição | Sessão, papel, dado existente necessário |
| Passos | Sequência de acções na UI |
| Resultado esperado | O que deve ser observável na tela/rede ao final |

Cobrir, por módulo aplicável:

- **CRUD** — criação, consulta (lista + detalhe), edição, exclusão, incluindo o modal de confirmação e o item a desaparecer da lista depois.
- **Formulários** — obrigatórios, validação client-side vs. mensagem vinda da API, submit duplo (double-click/debounce).
- **Filtros / busca / paginação / ordenação** — resultado correcto, estado vazio, navegação entre páginas, combinação de filtros.
- **Navegação e RBAC** — redirecção para não autorizado com papel sem permissão; menus condicionais coerentes com o papel real do backend.
- **Feedback visual** — Loading/skeletons/spinner, toast de sucesso/erro, modal de confirmação, botão a desabilitar durante o envio.
- **Responsividade** — ao menos os fluxos críticos em mobile e desktop.

Ordem de prioridade quando o escopo for completo: **Auth/RBAC → Catálogo → Estoque → Vendas → Financeiro → Clientes → Marketplace → Dashboard.**

---

## 5. Fase 3 — Priorização e severidade

| Critério de prioridade | Peso |
| ---------------------- | ---- |
| Fluxo gera receita ou é pré-requisito de outro (login, cadastro de produto) | Alto |
| Exposto publicamente sem autenticação (catálogo) | Alto |
| Envolve RBAC ou dados sensíveis (admin, financeiro) | Alto |
| Alta frequência de uso pelo utilizador final | Médio |
| Tela de configuração pouco acedida | Baixo |

Executar **Crítica → Alta → Média → Baixa**. Se o tempo ou o ambiente limitar, documentar em "Fluxos ainda não testados" (§8) — **nunca omitir silenciosamente**.

| Severidade | Critério |
| ---------- | -------- |
| **Bloqueante** | Impede o fluxo crítico de concluir (não é possível logar, não é possível cadastrar) |
| **Crítica** | Fluxo conclui mas com dado incorrecto/perdido, ou falha de segurança/RBAC |
| **Alta** | Funcionalidade quebrada mas com contorno, ou erro visível ao utilizador sem explicação |
| **Média** | Comportamento incorrecto sem bloquear o fluxo (mensagem errada, estado visual inconsistente) |
| **Baixa** | Cosmético, UX subóptima, sem impacto funcional |

Reprodutibilidade: **Sempre** / **Intermitente** / **Uma vez** — registar os passos exactos mesmo quando intermitente.

---

## 6. Fase 4 — Execução

Delegar ao subagent `e2e-qa-engineer` **um módulo por vez, sequencialmente e em foreground** —
nunca em paralelo: todos partilham a mesma aba e sessão autenticada. Em cada prompt de delegação, informar apenas:

1. O módulo em escopo e os cenários dessa fatia.
2. O estado da sessão (autenticada como que papel) e o `tabId`/URL onde continuar.
3. Restrições de dados acordadas no Passo 0.

Aguardar cada módulo terminar antes de iniciar o próximo.

Regras de execução que o agent aplica (definidas aqui, não repetir no prompt):

- **Incremental** — um cenário por vez; não acumular interações não relacionadas antes de validar.
- **Validação efectiva** — conferir o dado/estado real (texto da página, item na lista, status de rede). Página carregada **não** aprova o cenário.
- **Cadência de checagem** — em toda acção que dispara rede (submit, exclusão, filtro), conferir depois: mensagens no console (erros novos) e, se o feedback visual for ambíguo, o status real da rede. Um toast genérico pode esconder um 500.
- **Não ignorar ruído** — erro no console ou 4xx/5xx que não impediu a navegação ainda é bug; registar.
- **Evidência em toda falha** — screenshot/zoom na região relevante, ou leitura do texto exacto, antes de seguir.

### 6.1 Dados e segurança

- **Nunca** usar credenciais reais de produção ou dados de utilizadores reais. Usar contas de teste existentes ou criar dados descartáveis com prefixo **`[QA]`** para facilitar limpeza.
- **Acções irreversíveis** (excluir registo real, envio que notifica terceiros) exigem confirmação do utilizador antes, a menos que o dado seja de teste criado nesta execução.
- Não contornar RBAC/guards manipulando estado do cliente — testar controlo de acesso **através** da UI (tentar a rota sem permissão e confirmar bloqueio/redirecção).

---

## 7. Template de defeito

```
**Funcionalidade:** <módulo/tela>
**Passo realizado:** <acção exacta que disparou o problema>
**Comportamento esperado:** <o que deveria acontecer>
**Comportamento encontrado:** <o que de facto aconteceu>
**Evidência:** <screenshot/zoom, trecho de console ou network>
**Severidade:** Bloqueante | Crítica | Alta | Média | Baixa
**Reprodutibilidade:** Sempre | Intermitente | Uma vez
```

---

## 8. Passo final — Consolidação e relatório

Depois de todos os módulos do escopo, consolidar os relatórios individuais num único, com esta estrutura obrigatória:

1. **Resumo executivo** — cenários executados / aprovados / reprovados / bloqueados; recomendação final **apto** / **apto com ressalvas** / **não apto** para release, com justificativa de 1–2 frases.
2. **Cenários executados** — tabela ID / Módulo / Resultado (Aprovado / Reprovado / Bloqueado).
3. **Bugs encontrados** — ordenados por severidade, no template §7.
4. **Fluxos ainda não testados** — o que ficou de fora e porquê (tempo, ambiente, dado indisponível).
5. **Riscos identificados** — o que a execução não conseguiu garantir.
6. **Evidências** — referência às capturas, associadas ao ID do cenário/bug.

Gravar em `docs/qa/e2e-regression-<YYYY-MM-DD-HHmm>.md` (criar `docs/qa/` se não existir) e resumir no chat, destacando Bloqueante/Crítica primeiro e apontando o ficheiro.

---

## 9. Fora de escopo

- Testes unitários/integração automatizados — agent `test-engineer`.
- Revisão estática de diff — agent `code-reviewer`.
- Pentest, bypass de CAPTCHA, força bruta.
- Alterar configurações de segurança, permissões ou dados de produção.
- **Criar issues no tracker** — exige confirmação explícita do utilizador; nunca publicar sozinho.

---

## 10. Idioma

Relatório e comunicação em **português (Brasil)**; IDs de cenário em formato curto (`E2E-CATALOG-003`).

---

## Histórico

| Versão | Mudança |
| ------ | ------- |
| 3.0.0 | Movida para `.claude/skills/` (passa a ser carregável); formato alinhado ao EmpregaNetAPI com metodologia completa |
| 2.0.0 | Expansão: princípios, cenários, relatório |
| 1.0.0 | Versão inicial básica |
