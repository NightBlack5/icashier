# Spec Delta

## Purpose

Permite que o usuário retome as conversas do Jarvis após atualizar a página ou retornar ao assistente, mantendo o histórico disponível no mesmo navegador.

## ADDED Requirements

### Requirement: persistir conversas localmente
O sistema SHALL salvar no navegador as conversas do Jarvis que contenham mensagens enviadas e respostas recebidas.

#### Scenario: mensagem respondida
- **WHEN** o Jarvis conclui uma resposta para uma mensagem do usuário
- **THEN** a conversa atual é gravada no armazenamento local do navegador

#### Scenario: nova conversa sem mensagens do usuário
- **WHEN** o usuário inicia uma nova conversa sem enviar uma mensagem
- **THEN** o sistema não cria uma entrada vazia no histórico

### Requirement: restaurar histórico
O sistema SHALL restaurar as conversas salvas quando o usuário abrir a página do Jarvis.

#### Scenario: retorno à página
- **WHEN** o usuário autenticado abre ou atualiza a página do Jarvis
- **THEN** as conversas salvas são exibidas no histórico e a conversa selecionada é restaurada quando aplicável

#### Scenario: armazenamento ausente ou inválido
- **WHEN** não há histórico salvo ou o conteúdo salvo não é um JSON de conversas válido
- **THEN** o Jarvis inicia com uma conversa nova e o app continua funcionando sem exibir erro técnico

### Requirement: limitar histórico
O sistema SHALL manter no máximo oito conversas e vinte mensagens por conversa no armazenamento local.

#### Scenario: histórico excede o limite
- **WHEN** uma nova conversa faz o histórico ultrapassar oito itens
- **THEN** o item mais antigo é removido e cada conversa permanece limitada a vinte mensagens
