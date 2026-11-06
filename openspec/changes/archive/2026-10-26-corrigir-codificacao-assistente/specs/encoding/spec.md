# Codificação de textos

## ADDED Requirements

### Requirement: preservar português
O código da assistente SHALL manter textos em UTF-8 válido e não deve exibir
marcadores de dupla codificação.

#### Scenario: saudação renderizada
- **WHEN** a tela da assistente é carregada
- **THEN** a saudação exibe "Olá", "você" e "finanças" corretamente

### Requirement: detectar regressão
Os testes SHALL detectar marcadores de mojibake no estado da aplicação.

#### Scenario: arquivo corrompido
- **WHEN** `state.py` contém `Ã`, `Â` ou `�`
- **THEN** o teste falha
