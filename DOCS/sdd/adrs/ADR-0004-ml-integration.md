# ADR 0004: Integração Mercado Livre — Webhooks + API REST

**Status**: proposto
**Data**: 2026-08-26
**Decidido por**: Tech Lead + PO

## Contexto

O MVP do SG-MULTIDIA é publicar produtos no Mercado Livre e trazer dados
de pedidos/estoque para o dashboard. A integração é o core do produto.

## Decisão

- **API REST do ML** para publicação de produtos (`POST /items`)
- **Webhooks do ML** para notificações de pedidos e mudanças de estoque
- **Worker Go** para consumir webhooks e sincronizar dados
- **Kafka** como fila entre webhooks e backend (decoupling)
- **Rate limiting** no worker para respeitar limits da API do ML
- **Retry com backoff** para falhas transitórias
- **Token refresh** automático (ML usa OAuth 2.0)

## Consequências

- Fica fácil: publicação automatizada, sync em tempo real, dados sempre atualizados
- Fica difícil: manter tokens OAuth, tratar rate limits, lidar com inconsistências
- Risco: mudanças na API do ML podem quebrar integração

## Alternativas consideradas

- **Polling**: latência alta, desperdício de resources
- **SDK oficial do ML**: não existe para Java/Go nativamente
- **Integração direta no backend**: acoplaria o core ao ML (dificultaria trocar marketplace)
