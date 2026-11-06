# Design

## Context

`XanoAPIError` já preserva o código HTTP da resposta. O fluxo de autenticação atualmente exibe `str(error)` diretamente, permitindo que a mensagem e os detalhes do plano do Xano apareçam na interface.

## Goals / Non-Goals

**Goals:**

- Tratar HTTP 429 especificamente no método de autenticação.
- Manter mensagens genéricas para falhas de credenciais e preservar o diagnóstico técnico apenas no backend.

**Non-Goals:**

- Alterar o limite do plano Xano.
- Implementar bypass ou repetição automática de requisições.

## Decisions

- Mapear `status_code == 429` para uma mensagem fixa em português no estado da aplicação.
- Manter o comportamento existente para os demais erros, exceto credenciais já traduzidas pelo endpoint.

## Risks / Trade-offs

- [Risco] O limite pode continuar ativo por alguns segundos. -> Mitigação: explicar explicitamente que é temporário e evitar novas tentativas automáticas.
