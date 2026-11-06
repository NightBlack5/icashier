# Proposal

## Why

Nomes longos estão ultrapassando visualmente a largura disponível na barra lateral, invadindo o conteúdo principal.

## What Changes

- Reservar corretamente o espaço flexível do bloco do usuário.
- Truncar nomes longos com reticências dentro da largura da barra.
- Preservar o nome completo no atributo de acessibilidade/tooltip.

## Capabilities

### New Capabilities

- `sidebar-user-display`: exibição responsiva e contida da identidade do usuário na navegação.

### Modified Capabilities

- Nenhuma.

## Impact

- [CashSave/CashSave.py](../../../CashSave/CashSave.py)
- [CashSave/pages/assistente.py](../../../CashSave/pages/assistente.py)
- [CashSave/pages/financas.py](../../../CashSave/pages/financas.py)
