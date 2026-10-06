# Proposta: criar-layout-navegacao

## Why

Todas as telas do CashSave compartilham a mesma estrutura visual: uma barra lateral com o menu e uma área de conteúdo. É preciso criá-la antes das telas.

## What Changes

- Criar a barra lateral com os itens Visão Geral, Assistente IA, Finanças, Calendário, Sobre, Suporte e Apoiar o CashSave.
- Destacar o item da tela atual.
- Criar o rodapé com o bloco do usuário (dados de exemplo).

Fora do escopo desta mudança: autenticação e dados reais do usuário; as telas Finanças, Calendário e Sobre.

## Capabilities

### New Capabilities
- `app-navigation`: Permitir que o usuário navegue entre as telas do CashSave por uma barra lateral comum a todas as páginas.

### Modified Capabilities
- Nenhuma.

## Impact

- Projeto: CashSave (Python + Reflex, backend em Xano).
- Referência visual: capturas da versão antiga (Base44). Nenhum código copiado.
