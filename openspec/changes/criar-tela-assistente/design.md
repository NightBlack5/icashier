# Design: criar-tela-assistente

## Context

O CashSave terá um assistente de IA chamado Fin. Antes de integrar uma IA, a interface do chat precisa existir.

## Decisions

1. A integração com IA fica para uma mudança futura, porque depende de escolher o provedor, onde guardar a chave e quem arca com o custo.
2. A chave de qualquer provedor deverá ficar no backend (Xano), nunca no código do frontend.

Nota de processo: esta mudança foi documentada em formato OpenSpec depois de a implementação já ter sido feita. As mudanças seguintes seguem a ordem proposta, specs, design, tarefas e só então código.
