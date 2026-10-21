# Upload automático de avatar

## ADDED Requirements

### Requirement: enviar ao selecionar
O componente de foto SHALL iniciar o envio ao selecionar ou soltar um arquivo
válido.

#### Scenario: selecionar imagem válida
- **WHEN** uma pessoa autenticada seleciona PNG, JPG ou WebP
- **THEN** o handler de upload é acionado sem exigir outro clique

### Requirement: preservar reenvio e erros
O sistema SHALL manter o botão de reenvio e SHALL exibir falhas do Xano sem
informar sucesso falso.

#### Scenario: backend rejeita upload
- **WHEN** o endpoint de avatar retorna erro
- **THEN** a interface exibe a mensagem de erro e mantém o avatar anterior
