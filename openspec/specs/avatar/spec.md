# avatar Specification

## Purpose

TBD: Update Purpose after archive.

## Requirements

### Requirement: enviar ao selecionar

O componente de foto SHALL iniciar o envio ao selecionar ou soltar um arquivo válido.

#### Scenario: selecionar imagem válida

- **WHEN** uma pessoa autenticada seleciona PNG, JPG ou WebP
- **THEN** o handler de upload é acionado sem exigir outro clique

### Requirement: preservar reenvio e erros

O sistema SHALL manter o botão de reenvio e SHALL exibir falhas do Xano sem informar sucesso falso.

#### Scenario: backend rejeita upload

- **WHEN** o endpoint de avatar retorna erro
- **THEN** a interface exibe a mensagem de erro e mantém o avatar anterior

### Requirement: habilitar seleção autenticada

O sistema SHALL habilitar os controles de foto para uma sessão autenticada, mesmo quando o resumo não contiver `avatar_url`.

#### Scenario: resumo sem avatar

- **WHEN** a pessoa autenticada abre Preferências e o resumo não contém `avatar_url`
- **THEN** o seletor e o botão de envio permanecem habilitados

### Requirement: confirmar upload

O sistema SHALL atualizar o avatar somente após o endpoint retornar uma URL válida e SHALL mostrar o erro do backend quando o upload falhar.

#### Scenario: upload confirmado

- **WHEN** o Xano retorna uma URL válida
- **THEN** o avatar da interface é atualizado

#### Scenario: endpoint ausente

- **WHEN** o Xano rejeita `POST /auth/avatar`
- **THEN** a interface mostra a falha e não informa sucesso

