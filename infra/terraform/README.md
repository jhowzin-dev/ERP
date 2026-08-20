# SG-MULTIDIA — Terraform (AWS)
#
# Estrutura inicial. Implementação planejada para a fase de infraestrutura
# (ver Kanban-Desenvolvimento.kanban.md).
#
# Fases previstas (cada uma em seu diretório):
#   network/   VPC, subnets, security groups
#   database/  Aurora PostgreSQL, ElastiCache Redis
#   messaging/ Amazon MSK (Kafka), SQS + DLQ, S3
#   app/       ECS Fargate (backend + ingestion), Cognito, Secrets Manager
#   observability/ OpenTelemetry Collector, Grafana, Prometheus, Loki, Sentry
#
# Backend remoto e state locking (S3 + DynamoDB) devem ser configurados aqui
# quando o ambiente AWS estiver disponível. [A DEFINIR]