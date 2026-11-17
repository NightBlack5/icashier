# Spec Delta

## ADDED Requirements

### Requirement: Atalho flutuante para o Jarvis

O shell autenticado SHALL oferecer um botão flutuante de acesso ao Jarvis nas telas em que ele não concorra com um fluxo prioritário. O botão SHALL abrir a rota existente `/assistente`, sem criar outra conversa ou integração.

#### Scenario: Acesso rápido em uma tela autenticada

- **WHEN** a pessoa autenticada abre uma tela elegível do aplicativo
- **THEN** o botão flutuante do Jarvis permanece disponível durante a rolagem

#### Scenario: Abrir o Jarvis existente

- **WHEN** a pessoa ativa o botão flutuante
- **THEN** o aplicativo abre `/assistente` e restaura a conversa pelo fluxo existente

### Requirement: Atalho responsivo e acessível

O botão SHALL oferecer um nome acessível, tooltip ao receber foco ou hover e uma área de toque confortável, sem causar rolagem horizontal ou encobrir controles prioritários. Movimento não essencial SHALL ser reduzido quando `prefers-reduced-motion` estiver ativo.

#### Scenario: Uso em tela estreita ou com movimento reduzido

- **WHEN** a pessoa usa o atalho em dispositivo estreito ou com movimento reduzido
- **THEN** o botão continua identificável e acionável sem animação contínua ou overflow horizontal

### Requirement: Prioridade de fluxos e estado do assistente

O botão SHALL ficar ausente em telas sem autenticação e nas rotas `/assistente` e `/perfil`, e SHALL ficar abaixo de diálogos ativos. Ele SHALL exibir um indicador de presença somente se houver uma fonte confiável para esse estado.

#### Scenario: Tela ou diálogo prioritário

- **WHEN** a pessoa está em uma tela não autenticada, na página do Jarvis, em Preferências ou abre um diálogo
- **THEN** o atalho não concorre com o conteúdo ou com os controles do diálogo

#### Scenario: Estado de disponibilidade desconhecido

- **WHEN** o aplicativo não dispõe de um estado confiável de disponibilidade do Jarvis
- **THEN** o botão não afirma que o assistente está online
