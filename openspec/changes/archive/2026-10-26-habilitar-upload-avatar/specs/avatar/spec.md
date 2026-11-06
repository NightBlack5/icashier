# Foto de perfil

## ADDED Requirements

### Requirement: habilitar seleção autenticada
O sistema SHALL habilitar os controles de foto para uma sessão autenticada,
mesmo quando o resumo não contiver `avatar_url`.

#### Scenario: resumo sem avatar
- **WHEN** a pessoa autenticada abre Preferências e o resumo não contém `avatar_url`
- **THEN** o seletor e o botão de envio permanecem habilitados

### Requirement: confirmar upload
O sistema SHALL atualizar o avatar somente após o endpoint retornar uma URL
válida e SHALL mostrar o erro do backend quando o upload falhar.

#### Scenario: upload confirmado
- **WHEN** o Xano retorna uma URL válida
- **THEN** o avatar da interface é atualizado

#### Scenario: endpoint ausente
- **WHEN** o Xano rejeita `POST /auth/avatar`
- **THEN** a interface mostra a falha e não informa sucesso
