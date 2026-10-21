# URL do avatar

## ADDED Requirements

### Requirement: aceitar metadados Xano
O sistema SHALL extrair uma URL utilizável dos metadados de arquivo retornados
pelo Xano.

#### Scenario: resposta com URL pública
- **WHEN** o Xano retorna `avatar_url` com `url` ou `public_url`
- **THEN** a interface atualiza o avatar com essa URL

### Requirement: não mascarar resposta inválida
O sistema SHALL rejeitar respostas sem URL e informar que o Xano não retornou
uma URL utilizável.

#### Scenario: metadado sem URL
- **WHEN** o Xano confirma o upload mas não retorna URL
- **THEN** o avatar anterior permanece e a interface mostra erro
