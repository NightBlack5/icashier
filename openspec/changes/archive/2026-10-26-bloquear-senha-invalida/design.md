# Design

## Context

O schema remoto confirma que `user.password` é um campo de senha com hash. O endpoint observado trata a expressão da precondition como condição de interrupção, portanto a condição precisa ser a expressão de senha inválida.

## Goals / Non-Goals

**Goals:**

- Rejeitar senha inválida e aceitar senha correta.
- Confirmar que o documento publicado é o documento remoto.

**Non-Goals:**

- Alterar schema, usuários, hashes, cadastro ou tokens.

## Decisions

- Usar `precondition ($password_valid == false)` para representar a condição que deve interromper o stack neste workspace.
- Verificar o arquivo remoto após o push com pull do workspace.

## Risks / Trade-offs

- [Risco] Testes repetidos podem acionar o limite de requisições. -> Mitigação: validar o documento remoto sem repetir logins.
