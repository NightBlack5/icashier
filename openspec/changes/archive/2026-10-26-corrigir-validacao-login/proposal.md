# Proposal

## Why

O login rejeita credenciais válidas porque a condição da rota Xano interpreta o resultado da verificação de senha ao contrário. Isso impede usuários existentes de acessar o aplicativo.

## What Changes

- Corrigir a condição de validação da senha no endpoint `POST /auth/login`.
- Preservar a rejeição de e-mail inexistente ou senha inválida com mensagem genérica.
- Publicar somente a rota de login corrigida e validar o fluxo.

## Capabilities

### New Capabilities

- `user-authentication`: autenticação de usuários com credenciais válidas e rejeição segura de credenciais inválidas.

### Modified Capabilities

- Nenhuma.

## Impact

- [xano/api/cashsave/auth/login_POST.xs](../../../xano/api/cashsave/auth/login_POST.xs)
- Workspace Xano do CashSave.
- Testes e compilação da aplicação.
