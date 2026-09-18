# ADR 0005: Infraestrutura — CI/CD com Docker, GHCR, Terraform e VPS Oracle

**Status**: aceito (F1+F2) · decidido — implementação pendente (F3–F5)
**Data**: 2026-09-17
**Decidido por**: dono do projeto (arquitetura aprovada) + implementação java-implementer

## Contexto

O OminiCore é um monorepo de estudo (backend Java/Spring Modulith, frontend
React/Vite, ingestion Go) que evoluía com deploy ad hoc: SSH na VPS, `git pull`
e `docker compose up -d --build` na própria máquina de produção. Isso não escala
nem ensina o pipeline que o projeto pretende praticar: **build imutável no CI →
registry → deploy declarativo (Terraform) → TLS + hardening**.

Restrições do objetivo:

- Projeto de estudo, orçamento zero: VPS no **Always Free** da Oracle Cloud.
- Monorepo: três artefatos (`backend`, `frontend`, `ingestion`) com pipelines
  independentes e paths filtrados.
- Sem domínio comprado; sem IP fixo para o dono.
- Manter o harness local (`harness.ps1`/`harness.sh`) como porta de QA local.

## Decisões (numeradas)

1. **CI nativo + job `image` separado nos 3 workflows.** Os testes continuam
   rodando nativos no runner (Maven/npm/Go), sem Docker no meio do caminho, e um
   job `image` novo (`docker/build-push-action`) só roda em `push` para `main`,
   com `needs: <job-de-teste>`.
   - *Por quê:* cache nativo de Maven/npm/Go é mais rápido e estável do que
     cache de camadas Docker para testes; a equivalência "testou o que publica"
     é garantida pelo `needs:` — a imagem só é construída se os testes do mesmo
     commit passarem. Testar dentro do container dobraria o tempo de feedback
     sem ganho real aqui.
2. **GHCR como registry.** Login no CI com `GITHUB_TOKEN`
   (`permissions: packages: write` no workflow); tags `:latest` +
   `:sha-<commit>`; plataformas `linux/amd64,linux/arm64` (a VPS é ARM64).
3. **Kafka KRaft single-node na VPS** (`apache/kafka:3.8.0`, sem Zookeeper),
   `KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1`, `auto.create.topics=true`,
   volume persistente, limite 768M.
   - *Risco assumido:* RF=1 significa perda dos eventos se o volume morrer.
     Aceito porque o **Postgres é a fonte de verdade** e os eventos (pedidos,
     estoque) são re-sincronizáveis a partir do marketplace.
4. **Caddy como reverse proxy + TLS** (única porta pública: 80/443). Rota
   `/api/*` → `backend:8080`; resto → `frontend:80`. Nenhuma porta interna
   publicada (5432/9092/8080/8081 ficam na rede `ominicore`).
   - *Nota:* hoje não existe nenhum controller implementado — `/api/*` segue a
     convenção do backend-skill (`/api/{modulo}/{recurso}`). O actuator não é
     exposto pelo Caddy; o smoke test de prod roda dentro da rede.
5. **Compose dev e compose prod separados.** `backend/docker-compose.yml`
   permanece o stack de desenvolvimento (Zookeeper, Kafdrop, porta 5432
   publicada). Produção usa `infra/docker-compose.prod.yml` com imagens GHCR
   (`pull_policy: always`) — build nunca acontece na VPS.
6. **`harness.yml` aposentado.** O workflow que rodava os 3 módulos em sequência
   era redundante com `backend.yml` / `frontend.yml` / `ingestion.yml`
   (paths filtrados + jobs nativos). O harness **local** permanece.
7. **`deploy.yml` legado desativado.** Gatilho automático em `main` removido
   (resta apenas `workflow_dispatch`, marcado para reescrita na F4). O fluxo
   antigo (build na VPS) deixa de existir como caminho de deploy.

## Decisões do dono (2026-09-17)

Bloco registrado conforme aprovado pelo dono do projeto nesta data:

- **VPS**: Oracle Cloud **Ampere A1** (`VM.Standard.A1.Flex`, **ARM64**, Always
  Free — até 4 OCPU / 24 GB RAM). Por isso a exigência multi-arch no CI.
- **Terraform state**: **HCP Terraform** (Terraform Cloud), workspace único
  `ominicore-prod`. Nada de state em S3/OCI Object Storage nem local.
- **Domínio**: **sslip.io** — `<ip>.sslip.io` no Caddy, sem compra de domínio.
- **SSH (porta 22)**: temporariamente liberada para **`0.0.0.0/0`** porque o IP
  do dono é dinâmico. **Risco aceito formalmente + dívida técnica registrada**:
  antes de considerar F5 concluída, entregar a automação de whitelist de SSH
  (script/Action que atualiza a security list da OCI quando o IP muda **ou**
  fail2ban + chave única). Até lá, porta 22 aberta ao mundo é conhecida e
  monitorada; acesso APENAS por chave (sem senha).

## Roadmap F1–F5 (critério de pronto por fase)

| Fase | Escopo | Critério de pronto | Status |
| ---- | ------ | ------------------ | ------ |
| **F1** | Base Docker: Dockerfiles multi-arch dos 3 módulos + `infra/docker-compose.prod.yml` + Caddyfile + `.env.example` | `docker compose -f infra/docker-compose.prod.yml config` válido; Dockerfiles com `--platform=$BUILDPLATFORM` | ✅ concluída (2026-09-17) |
| **F2** | CI consolidado: job `image` nos 3 workflows, GHCR multi-arch; `harness.yml` removido; `deploy.yml` sem gatilho automático | Push em `main` publica as 3 imagens em GHCR com tags `:latest` + `:sha-<commit>` | ✅ concluída (2026-09-17) |
| **F3** | Terraform OCI (VCN, security list, compute A1, cloud-init) com state no HCP Terraform | `terraform plan/apply` reproduz a VPS do zero; outputs (IP público) registrados | ⏳ pendente |
| **F4** | CD: reescrever `deploy.yml` (SSH na VPS + `docker compose pull && up -d` das imagens GHCR) | Deploy de um commit de `main` pelo Actions sem build na VPS | ⏳ pendente |
| **F5** | TLS + domínio (`<ip>.sslip.io`) + hardening (fechar/atenuar SSH 0.0.0.0/0, UFW/security list revisada, atualizações automáticas) | HTTPS válido no domínio; dívida do SSH resolvida | ⏳ pendente |

## Consequências

- **Fica fácil:** deploy reproduzível por imagem imutável; rollback = apontar
  para `:sha-<commit>` anterior; CI rápido com cache nativo; VPS ARM64 barata
  (grátis) com imagens multi-arch garantidas; observação clara de quem publica
  o quê (um workflow por módulo).
- **Fica difícil:** sem pasta `db/migration` ainda, o backend sobe em prod com
  `ddl-auto=create` e Flyway desligado (**[VALIDAR]** — dívida registrada em
  `infra/docker-compose.prod.yml`: migrar para `JPA_DDL_AUTO=validate` +
  `FLYWAY_ENABLED=true` quando as migrations existirem); rodar multi-arch no CI
  aumenta o tempo do job `image` (build QEMU para arm64); operar Kafka KRaft
  single-node exige aceitar a possibilidade de perda de eventos em desastre.

## Riscos

- **Capacidade Ampere A1 indisponível** (frequente em regiões disputadas):
  tentar outro AD/região; o Terraform parametriza shape/AD.
- **Reclaim da VM free** (OCI pode reclamar instâncias ociosas): recriação é
  `terraform apply` + `compose pull/up`; dados em volumes + re-sync dos eventos.
- **Perda de state Terraform**: HCP Terraform guarda o histórico de states —
  recuperação via plataforma, sem locks manuais.
- **SSH 0.0.0.0/0 aberto**: mitigação parcial = apenas chave, sem senha;
  resolução definitiva é a automação de whitelist antes do fim da F5.

## Alternativas consideradas

- **Testes dentro do container (job único)**: feedback mais lento, cache de
  dependências pior; rejeitado em favor de CI nativo + `needs:`.
- **Docker Hub**: rate limits e credenciais extras; GHCR usa `GITHUB_TOKEN` e
  vive ao lado do código.
- **Zookeeper (stack Confluent)**: mais um serviço (256M+ de RAM) sem benefício
  em single-node; KRaft é o caminho oficial do Kafka.
- **nginx + certbot manual**: mais peças para TLS; Caddy resolve certificado e
  renovação com 3 linhas.
- **State Terraform local ou em Object Storage**: state local se perde com a
  máquina; bucket próprio exige configurar lock e acesso — HCP Terraform dá
  state gerenciado + histórico no plano gratuito.
- **Domínio comprado**: custo desnecessário para projeto de estudo; sslip.io
  resolve com zero custo.
