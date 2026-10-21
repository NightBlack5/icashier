# Proposal

## Why

Quando o plano do Xano limita tentativas de login, o aplicativo exibe a mensagem técnica em inglês diretamente na tela. Isso confunde o usuário e não informa claramente que basta aguardar a liberação temporária.

## What Changes

- Traduzir e normalizar respostas HTTP 429 no fluxo de autenticação.
- Informar que o bloqueio é temporário e indicar o tempo aproximado de espera.
- Não exibir detalhes técnicos ou links internos do provedor na tela de login.

## Capabilities

### New Capabilities

- `login-rate-limit-feedback`: feedback seguro e compreensível para limitação temporária de tentativas de login.

### Modified Capabilities

- Nenhuma.

## Impact

- [CashSave/state.py](../../../CashSave/state.py)
- Testes do fluxo de autenticação.
