---
version: 1
status: draft
---

# PRD — Dashboard de Gestão

## 1. Problema

O gestor/vendedor não tem visão centralizada do desempenho do negócio. Precisa
abrir múltiplas telas para ver vendas, estoque, pedidos e publicações no ML.
Não há indicadores em tempo real nem alertas de problemas (estoque baixo,
pedidos pendentes).

## 2. Personas

| Persona | O que faz com esta feature |
|---------|---------------------------|
| Gestor | Acompanha KPIs diários, identifica problemas, toma decisões rápidas |
| Vendedor | Vê resumo de vendas, estoque baixo, pedidos para faturar |

## 3. Funcionalidades

### 3.1 Visão geral (home do dashboard)
- **Como** gestor, **quero** ver na tela principal: vendas do dia, receita, estoque baixo, pedidos pendentes, **para ter** visão instantânea do negócio.
  - **CA**: Dados atualizados em tempo real (polling a cada 30s ou WebSocket).
  - **CA**: Cards com números grandes e cores semântico (verde = OK, vermelho = atenção).

### 3.2 Gráfico de vendas
- **Como** gestor, **quero** ver gráfico de vendas dos últimos 7/30 dias, **para** identificar tendências.
  - **CA**: Gráfico de linha com vendas por dia.
  - **CA**: Filtro por período (7d, 30d, 90d).
  - **CA**: Comparativo com período anterior (seta para cima/baixo).

### 3.3 Alerta de estoque baixo
- **Como** vendedor, **quero** ser alertado quando estoque estiver abaixo do mínimo, **para** evitar ruptura.
  - **CA**: Badge/card no dashboard com quantidade de itens com estoque baixo.
  - **CA**: Lista clicável levando à tela de catálogo filtrada.

### 3.4 Pedidos recentes
- **Como** vendedor, **quero** ver os últimos pedidos (internos + ML) no dashboard, **para** saber o que faturar/enviar.
  - **CA**: Lista dos 5 pedidos mais recentes com status.
  - **CA**: Link para detalhe do pedido.

### 3.5 Resumo ML
- **Como** gestor, **quero** ver: produtos publicados no ML, vendas ML hoje, **para** acompanhar o canal online.

## 4. Métricas de sucesso

| Métrica | Meta |
|---------|------|
| Tempo de carregamento do dashboard | < 2 segundos |
| Frequência de atualização | < 30 segundos (polling) |
| Uso diário (gestores) | > 80% dos gestores acessam diariamente em 30 dias |

## 5. Fora de escopo (MVP)

- Exportação de relatórios (PDF/Excel)
- Dashboard personalizável (widgets arrastáveis)
- Metas e prognósticos com IA
- Comparativo entre filiais/lojas

## 6. Pendências

- `[A DEFINIR]`: Quais KPIs exatos aparecem no card principal?
- `[VALIDAR]`: Dados do ML já estarão disponíveis via integração (depende de `ml-integration`)?
