# Design

## Context

O endpoint Xano usa `security.check_password` e uma precondition para bloquear credenciais inválidas. O comportamento observado confirma que a precondition configurada como verdadeira interrompe a execução.

## Goals / Non-Goals

**Goals:**

- Usar uma condição explicitamente falsa para bloquear apenas senhas inválidas.

**Non-Goals:**

- Alterar hashes, usuários, formulário, tokens ou limite do plano.

## Decisions

- Usar `precondition ($password_valid == false)` para que a precondition seja acionada somente quando a senha não corresponder.
- Publicar apenas `auth/login_POST.xs`.

## Risks / Trade-offs

- [Risco] O Xano pode manter uma sessão antiga no navegador. -> Mitigação: testar após sair da conta e limpar a sessão.
