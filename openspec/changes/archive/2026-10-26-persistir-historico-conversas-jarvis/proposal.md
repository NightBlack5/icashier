# Proposal

## Why

As conversas do Jarvis são mantidas apenas no estado da sessão Reflex. Ao atualizar a página ou sair e voltar ao assistente, a lista de histórico desaparece, impedindo o usuário de continuar conversas anteriores.

## What Changes

- Persistir as conversas do Jarvis no armazenamento local do navegador.
- Restaurar o histórico ao abrir a página do assistente.
- Atualizar o armazenamento sempre que uma conversa for criada, alterada ou iniciada novamente.
- Preservar os limites atuais de até oito conversas e vinte mensagens por conversa.

## Capabilities

### New Capabilities

- `jarvis-conversation-history`: persistência e restauração local do histórico de conversas do Jarvis.

### Modified Capabilities

- Nenhuma.

## Impact

- Estado Reflex e eventos da página do Jarvis.
- Armazenamento local do navegador.
- Testes de estado e compilação Reflex; nenhuma alteração de API do Xano.
