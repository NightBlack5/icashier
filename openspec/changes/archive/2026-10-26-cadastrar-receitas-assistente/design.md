# Design

## Context

O endpoint `POST /transacoes` já aceita os tipos `receita` e `despesa`. O parser local atualmente produz somente comandos de despesa e usa uma conversão incompleta para valores com escala e separadores brasileiros.

## Goals / Non-Goals

**Goals:**

- Produzir o tipo correto e o valor em centavos antes da chamada ao Xano.
- Reutilizar o mesmo fluxo autenticado de transações.

**Non-Goals:**

- Alterar o endpoint Xano ou o modelo de transações.
- Permitir que o modelo Ollama invente lançamentos.

## Decisions

- Estender o resultado do parser com `tipo`, mantendo o nome e a assinatura existentes para evitar mudanças desnecessárias no orquestrador.
- Interpretar escala `mil` e separadores brasileiros localmente, antes da persistência.

## Risks / Trade-offs

- [Risco] Frases ambíguas podem ser classificadas como receita. -> Mitigação: exigir verbos e termos explícitos de recebimento.
