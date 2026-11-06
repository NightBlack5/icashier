# Proposal

## Why

A condição comparada explicitamente com `false` está permitindo que uma senha inválida avance no login remoto. A rota deve usar o padrão de autenticação do Xano, exigindo diretamente o resultado válido da verificação antes de criar o token.

## What Changes

- Usar `$password_valid` diretamente na precondition do login.
- Publicar somente `POST /auth/login`.
- Preservar o token e a resposta atuais.

## Capabilities

### New Capabilities

- `xano-password-validation`: autenticação baseada no resultado oficial da validação de senha do Xano.

### Modified Capabilities

- Nenhuma.

## Impact

- [xano/api/cashsave/auth/login_POST.xs](../../../xano/api/cashsave/auth/login_POST.xs)
- Endpoint remoto de autenticação.
