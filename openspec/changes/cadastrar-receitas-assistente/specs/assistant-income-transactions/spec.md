# Spec Delta

## Purpose

Permite que o Jarvis registre receitas e despesas informadas pelo usuário, preservando valores, datas e tipo da transação.

## ADDED Requirements

### Requirement: cadastrar receita por linguagem natural
O sistema SHALL reconhecer comandos de recebimento e criar uma transação com tipo `receita`.

#### Scenario: salário informado
- **WHEN** o usuário diz “eu recebo 10 mil de salário dia 5”
- **THEN** o sistema cria uma receita de R$ 10.000,00 com descrição do salário

### Requirement: interpretar valores brasileiros
O sistema SHALL interpretar corretamente valores com escala “mil” e separadores brasileiros.

#### Scenario: valor em milhares
- **WHEN** o usuário informa “R$ 10.000,00”
- **THEN** o valor armazenado é 1.000.000 centavos

### Requirement: preservar despesas
O sistema SHALL continuar criando despesas com tipo `despesa` para comandos de gasto.

#### Scenario: gasto informado
- **WHEN** o usuário diz “gastei R$ 25,90 em transporte”
- **THEN** o sistema cria uma despesa de 2.590 centavos
