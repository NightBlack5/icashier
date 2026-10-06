# Design: criar-tela-suporte

## Context

O usuário precisa de um lugar para encontrar respostas rápidas e formas de contato com a equipe do CashSave.

## Decisions

1. As perguntas frequentes usam o componente de acordeão do Reflex, montado com uma lista Python (não com `rx.foreach`, que perde parte do estilo).
2. Contatos e links ficam em constantes no topo do bloco para facilitar a troca.
3. Os ícones das redes sociais são provisórios, pois a biblioteca de ícones não traz as logos oficiais.

Nota de processo: esta mudança foi documentada em formato OpenSpec depois de a implementação já ter sido feita. As mudanças seguintes seguem a ordem proposta, specs, design, tarefas e só então código.
