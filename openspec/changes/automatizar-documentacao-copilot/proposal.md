# Proposta: automatizar-documentacao-copilot

## Por que

As mudanças feitas pelo Copilot podem deixar as especificações OpenSpec desatualizadas se a documentação depender de um pedido manual separado.

## O que muda

- Adicionar instruções de repositório para o Copilot consultar as especificações e registrar cada solicitação de alteração de código no fluxo OpenSpec.
- Exigir que tarefas e especificações acompanhem a implementação e sua verificação.

Fora do escopo: monitorar alterações feitas manualmente ou por ferramentas externas ao Copilot.

## Capacidades

### Novas capacidades
- `copilot-openspec-workflow`: orientar o Copilot a manter o OpenSpec sincronizado com as mudanças que implementa neste repositório.

### Capacidades modificadas
- Nenhuma.

## Impacto

- Instruções do GitHub Copilot em `.github/copilot-instructions.md`.
- Fluxo de mudanças e especificações em `openspec/`.
