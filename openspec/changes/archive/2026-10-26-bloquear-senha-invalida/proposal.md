# Proposal

## Why

O endpoint remoto está rejeitando senhas corretas e permitindo senhas incorretas porque a precondition foi configurada com a expressão de senha válida. Neste workspace, a precondition interrompe quando sua expressão é verdadeira.

## What Changes

- Fazer a precondition representar explicitamente uma senha inválida.
- Publicar somente `POST /auth/login`.
- Puxar a rota após a publicação para confirmar o estado remoto.

## Capabilities

### New Capabilities

- `invalid-password-rejection`: rejeição de credenciais quando a senha não corresponde ao hash.

### Modified Capabilities

- Nenhuma.

## Impact

- [xano/api/cashsave/auth/login_POST.xs](../../../xano/api/cashsave/auth/login_POST.xs)
- Endpoint remoto de login.
