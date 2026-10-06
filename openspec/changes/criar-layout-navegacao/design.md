# Design: criar-layout-navegacao

## Context

Todas as telas do CashSave compartilham a mesma estrutura visual: uma barra lateral com o menu e uma área de conteúdo. É preciso criá-la antes das telas.

## Decisions

1. A estrutura é montada em Python/Reflex com a função `sidebar`, reutilizada por todas as telas.
2. O item ativo é decidido comparando a rota atual com a rota de cada item.
3. O bloco do usuário usa dados fixos ("Usuário") até existir autenticação.
4. Tema escuro com destaque verde, seguindo a referência visual.

## Risks / Trade-offs

Itens do menu sem tela ainda levam a uma página de rota não encontrada.

Nota de processo: esta mudança foi documentada em formato OpenSpec depois de a implementação já ter sido feita. As mudanças seguintes seguem a ordem proposta, specs, design, tarefas e só então código.
