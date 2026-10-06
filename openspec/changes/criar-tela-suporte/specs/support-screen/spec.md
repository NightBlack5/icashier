## Purpose

Apresentar a central de suporte com canais de contato e perguntas frequentes.

## ADDED Requirements

### Requirement: Canais de contato
O sistema SHALL exibir na rota `/suporte` os canais de contato de e-mail, WhatsApp e redes sociais.

#### Scenario: Abrir o suporte
- **WHEN** o usuário abre a rota `/suporte`
- **THEN** os três cartões de contato são exibidos

### Requirement: Perguntas frequentes
O sistema SHALL exibir uma lista de perguntas frequentes que podem ser expandidas e recolhidas.

#### Scenario: Expandir uma pergunta
- **WHEN** o usuário clica em uma pergunta frequente
- **THEN** a resposta correspondente é exibida
