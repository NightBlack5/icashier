# Proposal

## Why

O projeto possui documentação distribuída entre o README, relatórios de auditoria
e mudanças OpenSpec, enquanto a estrutura atual do aplicativo e suas limitações
não estão resumidas em um documento estável. O worktree também contém alterações
preexistentes que não podem ser misturadas com esta missão sem risco de perda ou
publicação indevida.

## What Changes

- Criar uma especificação factual em `spec/` sobre o estado atual do projeto.
- Atualizar o `README.md` com instalação, configuração, execução, testes e link
  para o Spec.
- Registrar no Spec as responsabilidades dos módulos, integrações, segurança,
  limitações e estado de implementação.
- Validar documentação, sintaxe, testes e compilação sem alterar os módulos
  centrais que já estavam modificados.
- Publicar somente os arquivos comprovadamente criados ou editados por esta
  missão, sem restaurar exclusões nem incluir o `.env`.

## Capabilities

### New Capabilities

Nenhuma. Esta é uma mudança de documentação, organização de escopo e validação;
ela não altera comportamento do aplicativo.

### Modified Capabilities

Nenhuma.

## Impact

- Documentação: `README.md` e `spec/`.
- Planejamento: este change OpenSpec.
- Código, dependências, APIs Xano e artefatos do portfólio: preservados.
- O commit deverá usar paths explícitos para excluir alterações preexistentes.
