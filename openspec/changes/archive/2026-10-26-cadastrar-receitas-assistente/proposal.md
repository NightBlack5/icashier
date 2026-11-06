# Proposal

## Why

O Jarvis já cadastra despesas, mas não reconhece comandos de receitas. Além disso, valores escritos como “10 mil” são interpretados incorretamente, impedindo lançamentos financeiros confiáveis.

## What Changes

- Reconhecer receitas em linguagem natural.
- Enviar receitas para o mesmo endpoint de transações com `tipo = receita`.
- Interpretar valores com “mil” e formatação monetária brasileira.
- Manter o cadastro de despesas existente.

## Capabilities

### New Capabilities

- `assistant-income-transactions`: cadastro de receitas e despesas por comandos naturais no assistente.

### Modified Capabilities

- Nenhuma.

## Impact

- [CashSave/ai_services.py](../../../CashSave/ai_services.py)
- [CashSave/state.py](../../../CashSave/state.py)
- Testes do parser financeiro.
