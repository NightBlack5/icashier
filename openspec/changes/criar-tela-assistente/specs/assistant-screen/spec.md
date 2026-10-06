## Purpose

Apresentar a interface do assistente financeiro Fin, sem resposta real nesta fase.

## ADDED Requirements

### Requirement: Tela Assistente IA
O sistema SHALL exibir na rota `/assistente` o cabeçalho do assistente Fin, uma mensagem de boas-vindas, três sugestões de perguntas e um campo de mensagem.

#### Scenario: Abrir o assistente
- **WHEN** o usuário abre a rota `/assistente`
- **THEN** a mensagem de boas-vindas, as três sugestões e o campo de mensagem são exibidos

### Requirement: Interface sem resposta nesta fase
O campo de mensagem e as sugestões SHALL ser apenas visuais e nenhuma resposta SHALL ser gerada.

#### Scenario: Enviar uma mensagem
- **WHEN** o usuário clica em uma sugestão ou no botão de envio
- **THEN** nenhuma resposta é gerada nesta fase
