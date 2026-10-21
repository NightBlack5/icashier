# Design

## Context

O endpoint usa `security.check_password` antes de `security.create_auth_token`. A expressão anterior com negação não apresentou comportamento confiável após a importação no Xano.

## Goals / Non-Goals

**Goals:**

- Exigir um resultado booleano verdadeiro para prosseguir.
- Evitar operadores ambíguos no parser da rota.

**Non-Goals:**

- Alterar usuários, hashes, expiração ou contrato de resposta.

## Decisions

- Usar `precondition ($password_valid == true)`, pois a precondition falha quando a expressão não é verdadeira e a comparação explicita a regra.
- Publicar somente a rota de login após preview.

## Risks / Trade-offs

- [Risco] O workspace pode conter referências não incluídas no push. -> Mitigação: limitar o arquivo publicado e verificar o preview antes do envio.
