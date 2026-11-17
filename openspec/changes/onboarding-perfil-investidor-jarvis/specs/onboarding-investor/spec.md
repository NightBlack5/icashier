## Purpose

Permitir que o CashSave colete informações financeiras iniciais do usuário, avalie seu perfil de investidor e mantenha o assistente Jarvis contextualizado sem exigir que o usuário responda tudo na primeira visita.

## ADDED Requirements

### Requirement: onboarding financeiro com progresso
O sistema SHALL oferecer um onboarding guiado com etapas numeradas, avanço e retorno, permitindo pular qualquer etapa e concluir parcialmente o cadastro sem obrigar respostas financeiras.

#### Scenario: Cadastro inicial com progresso
- **WHEN** o usuário acessa pela primeira vez a conta autenticada
- **THEN** o sistema exibe uma sequência de etapas com indicador de progresso e ações de avançar, voltar e pular

#### Scenario: Progresso salvo
- **WHEN** o usuário avança ou interrompe a configuração
- **THEN** o aplicativo salva automaticamente o estado atual e permite continuar depois

### Requirement: coleta de contexto financeiro
O sistema SHALL coletar renda, despesas, objetivos financeiros, reserva de emergência e dados de experiência com investimentos sem transformar respostas em zero ou dados assumidos.

#### Scenario: Usuário responde parcialmente
- **WHEN** o usuário pula perguntas ou deixa campos vazios
- **THEN** as informações permanecem como não informadas e não são interpretadas como zero

#### Scenario: coleta de múltiplas fontes de renda
- **WHEN** o usuário indica mais de uma fonte de renda
- **THEN** o sistema registra cada origem em conjunto com os valores aproximados informados

### Requirement: perfil de investidor contextualizado
O sistema SHALL avaliar o perfil do usuário com base em tolerância ao risco, conhecimento, experiência, horizonte, objetivos e capacidade financeira, classificando em conservador, moderado ou arrojado.

#### Scenario: perfil identificado
- **WHEN** o usuário conclui as respostas relevantes do onboarding
- **THEN** a aplicação mostra o perfil identificado, a explicação do resultado e os pontos de atenção

#### Scenario: atualização da avaliação
- **WHEN** a situação financeira do usuário muda ou ele refaz a avaliação
- **THEN** o perfil pode ser recalculado e atualizado sem bloquear o uso do aplicativo

### Requirement: assistente global sempre acessível
O sistema SHALL manter o Jarvis acessível a partir de um botão flutuante no canto inferior direito em telas autenticadas, sem criar uma IA separada ou remover o assistente atual.

#### Scenario: abertura do assistente global
- **WHEN** o usuário navega em qualquer tela autenticada
- **THEN** o botão flutuante do Jarvis permite abrir a conversa com o assistente do CashSave
