# Nome da assistente

## ADDED Requirements

### Requirement: exibir Jarvis
A interface SHALL chamar a assistente de Jarvis nos menus, cabeçalhos, título
da página e saudação inicial.

#### Scenario: abrir a página da assistente
- **WHEN** a pessoa abre `/assistente`
- **THEN** a página exibe o nome Jarvis

### Requirement: preservar funcionamento
A mudança de nome SHALL manter a rota `/assistente`, o envio por Enter e as
capacidades financeiras existentes.

#### Scenario: enviar mensagem
- **WHEN** a pessoa envia uma pergunta
- **THEN** a mensagem é processada pelo mesmo fluxo existente
