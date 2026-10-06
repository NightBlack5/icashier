# Proposta: criar-tela-visao-geral

## Why

A tela Visão Geral é a primeira que o usuário vê. Ela resume saldo, receitas, despesas e contas a pagar, e dá acesso rápido às demais áreas.

## What Changes

- Criar quatro cartões de resumo (Saldo do Mês, Receitas, Despesas, Contas a Pagar).
- Criar o gráfico dos últimos seis meses.
- Criar o card Próximos Vencimentos.
- Criar os atalhos de Acesso Rápido e o banner do assistente.

Fora do escopo desta mudança: dados reais, cálculo de saldo e leitura de transações (dependem de autenticação e do modelo de dados).

## Capabilities

### New Capabilities
- `overview-screen`: Apresentar a tela inicial do CashSave com o resumo financeiro, ainda com valores de exemplo.

### Modified Capabilities
- Nenhuma.

## Impact

- Projeto: CashSave (Python + Reflex, backend em Xano).
- Referência visual: capturas da versão antiga (Base44). Nenhum código copiado.
