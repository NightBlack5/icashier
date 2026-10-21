# Design

## Context

O Xano possui um fluxo padrão de autenticação com `security.check_password` seguido de uma precondition usando diretamente a variável booleana retornada. A comparação explícita anterior apresentou comportamento incorreto no workspace.

## Goals / Non-Goals

**Goals:**

- Reutilizar a forma padrão do Xano para validar a senha.
- Impedir emissão de token para senha inválida.

**Non-Goals:**

- Alterar usuários, hashes, cadastro ou expiração do token.

## Decisions

- Definir `precondition ($password_valid)` para alinhar a rota ao endpoint de autenticação padrão do Xano.
- Publicar somente o arquivo da rota de login após preview.

## Risks / Trade-offs

- [Risco] Usuários cadastrados com hash inválido continuarão sem conseguir entrar. -> Mitigação: preservar o fluxo de cadastro e tratar a correção de dados como tarefa separada.
