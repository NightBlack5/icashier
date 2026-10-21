# Proposal

## Why

A condição atual da precondition do Xano bloqueia senhas válidas porque está configurada para falhar quando a verificação retorna verdadeiro. A rota precisa bloquear somente resultados falsos.

## What Changes

- Alterar a precondition do login para bloquear apenas senha não correspondente.
- Publicar somente o endpoint `POST /auth/login`.
- Validar compilação e testes sem alterar dados de usuários.

## Capabilities

### New Capabilities

- `password-authentication-condition`: condição correta de aprovação e rejeição da senha no login.

### Modified Capabilities

- Nenhuma.

## Impact

- [xano/api/cashsave/auth/login_POST.xs](../../../xano/api/cashsave/auth/login_POST.xs)
- Endpoint remoto de login do Xano.
