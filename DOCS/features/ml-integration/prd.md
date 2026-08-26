---
version: 1
status: draft
---

# PRD — Integração Mercado Livre

## 1. Problema

O vendedor precisa publicar produtos no Mercado Livre manualmente, um a um,
perdendo tempo e cometendo erros de digitação. Não há sync de estoque/preço,
o que gera vendas de produto indisponível e preços desatualizados. Pedidos
chegam por e-mail e precisam ser digitados no sistema.

## 2. Personas

| Persona | O que faz com esta feature |
|---------|---------------------------|
| Vendedor/Lojista | Publica produtos em lote no ML, acompanha pedidos que chegam automaticamente |
| Gestor | Vê estoque e preço sempre atualizados, sem abertura manual |

## 3. Funcionalidades

### 3.1 Publicação de produtos no ML
- **Como** vendedor, **quero** selecionar produtos do catálogo e publicar no ML, **para que** eles apareçam à venda automaticamente.
  - **CA**: Produto publicado aparece no ML com título, descrição, preço, fotos e estoque corretos.
  - **CA**: Status do produto muda para "Publicado no ML" no catálogo interno.
  - **CA**: Erro na publicação é exibido com mensagem clara (ex.: "Título muito longo", "Preço abaixo do mínimo").

### 3.2 Sync de estoque
- **Como** vendedor, **quero** que o estoque no ML seja atualizado automaticamente quando há venda interna ou ajuste, **para que** não venda produto indisponível.
  - **CA**: Quando estoque interna diminui, ML é atualizado em < 5 minutos.
  - **CA**: Quando ML vende, estoque interno é decrementado.
  - **CA**: Conflito de estoque é registrado para revisão.

### 3.3 Sync de preço
- **Como** vendedor, **quero** alterar o preço interno e ele ser refletido no ML, **para que** preços estejam sempre corretos.
  - **CA**: Alteração de preço no catálogo propaga para ML em < 5 minutos.
  - **CA**: Preço no ML nunca fica desatualizado por mais de 10 minutos.

### 3.4 Recebimento de pedidos
- **Como** vendedor, **quero** que pedidos do ML apareçam automaticamente no sistema, **para que** eu não precise copiar manualmente.
  - **CA**: Pedido do ML chega via webhook e é registrado no sistema com todos os dados (comprador, itens, valor, frete).
  - **CA**: Status do pedido é "Novo" até que o vendedor tome ação.
  - **CA**: Pedido duplicado (mesmo ID ML) não é criado novamente.

### 3.5 Dashboard de resumo ML
- **Como** gestor, **quero** ver no dashboard: total de produtos publicados, vendas hoje no ML, estoque baixo, **para ter** visão rápida do desempenho.

## 4. Métricas de sucesso

| Métrica | Meta |
|---------|------|
| Tempo de publicação em lote | < 2 minutos para 50 produtos |
| Latência de sync de estoque | < 5 minutos (p95) |
| Taxa de webhook recebido com sucesso | > 99% |
| Redução de vendas de produto indisponível | > 90% em 30 dias |

## 5. Fora de escopo (MVP)

- Gestão de fotos (upload direto para ML)
- Otimização de títulos/descrições com IA
- Múltiplos marketplaces (Magazine Luiza, Amazon, etc.)
- Gestão de frete/cálculo de envio
- Reclamações/atendimento no ML

## 6. Pendências

- `[A DEFINIR]`: Endpoint exato do ML para publicação em lote (verificar limites de rate)
- `[A DEFINIR]`: Formato do webhook de pedidos do ML (payload completo)
- `[VALIDAR]`: ML permite atualização de estoque via API para qualquer item?
- `[VALIDAR]`: Token OAuth expira em quanto tempo? Precisa de refresh automático?
