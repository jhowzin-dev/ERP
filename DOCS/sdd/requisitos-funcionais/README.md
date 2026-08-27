# Requisitos Funcionais

> Pasta para especificações de requisitos funcionais do OminiCore.
> Cada requisito vive em um arquivo `.md` nesta pasta.

## Convenção

- Arquivos em `kebab-case` (ex: `rf-001-catalogo-produtos.md`)
- Cada arquivo segue o template de requisito funcional
- Versionamento via frontmatter

## Template

```markdown
---
id: RF-XXXX
version: 1
status: draft | in-review | approved
---

# RF-XXXX: <Título>

## Descrição
<o que o requisito faz>

## Critérios de aceite
- [ ] <critério 1>
- [ ] <critério 2>

## Prioridade
Alta | Média | Baixa

## Dependências
<requisitos ou ADRs relacionados>
```
