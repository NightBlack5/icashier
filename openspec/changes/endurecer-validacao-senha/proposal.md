# Proposal

## Why

A validação publicada com operador de negação não está protegendo o login como esperado. A condição precisa exigir explicitamente que o resultado da verificação de senha seja verdadeiro antes de criar uma sessão.

## What Changes

- Substituir a condição ambígua por uma comparação booleana explícita.
- Manter o erro genérico para credenciais inválidas.
- Publicar somente a rota de login.

## Capabilities

### New Capabilities

- `secure-login-validation`: validação explícita de senha antes da emissão de sessão.

### Modified Capabilities

- Nenhuma.

## Impact

- [xano/api/cashsave/auth/login_POST.xs](../../../xano/api/cashsave/auth/login_POST.xs)
- Endpoint remoto de autenticação do Xano.
