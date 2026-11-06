# assistant-batch-transactions Specification

## Purpose

TBD: Update Purpose after archive.

## Requirements

### Requirement: Register and calculate multiple stated transactions

O Jarvis SHALL identificar valores monetários e seus tipos de receita ou despesa
em uma mensagem que descreva lançamentos financeiros, validar todos os itens
antes de gravar, e enviar cada lançamento separadamente pelo endpoint
autenticado de transações. Ele SHALL usar apenas IDs de categorias e contas
carregados para o usuário e SHALL NOT inventar registros auxiliares.

Depois que todos os lançamentos forem confirmados pelo Xano, o Jarvis SHALL
calcular deterministicamente os totais de receitas, despesas e o saldo
(`receitas - despesas`) em centavos a partir dos itens informados, e SHALL
deixar claro que o resultado corresponde ao conjunto da mensagem.

#### Scenario: User reports income, expenses, and asks for the totals

- **WHEN** o usuário informa que recebeu R$ 2.500 de salário e gastou R$ 850 com
  aluguel, R$ 420 com mercado, R$ 180 com transporte, R$ 120 com internet e
  celular e R$ 250 com lazer, e pergunta quanto sobrou e qual foi o gasto total
- **THEN** o Jarvis envia uma receita de R$ 2.500,00 e cinco despesas separadas
  ao Xano, e informa despesas de R$ 1.820,00 e saldo dos lançamentos de
  R$ 680,00 somente após confirmar os seis registros

#### Scenario: User asks a question without stating transactions to register

- **WHEN** o usuário pergunta quanto gastou ou quanto sobrou sem declarar novos
  lançamentos financeiros
- **THEN** o Jarvis responde usando os dados financeiros carregados e não cria
  transações

#### Scenario: Xano confirms only part of the batch

- **WHEN** uma ou mais transações são confirmadas, mas uma transação posterior
  falha ou não retorna um ID
- **THEN** o Jarvis informa quantas foram confirmadas e qual item falhou, atualiza
  o estado local somente com as confirmações e não declara o lote inteiro como
  concluído

