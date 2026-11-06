# Armazenamento público do avatar

## ADDED Requirements

### Requirement: gerar URL pública
O endpoint SHALL criar metadados públicos para a imagem e salvar o resultado no
perfil autenticado.

#### Scenario: upload válido
- **WHEN** o endpoint recebe uma imagem válida
- **THEN** `avatar_url` contém os metadados com URL pública

### Requirement: responder com avatar
A resposta SHALL devolver o usuário atualizado incluindo `avatar_url`.

#### Scenario: upload confirmado
- **WHEN** o armazenamento e o patch do usuário são concluídos
- **THEN** a resposta contém a URL do avatar atualizado
