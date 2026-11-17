# Design

## Context

O shell comum é montado por `app_layout` em `CashSave/components/layout.py`. O atalho atual está definido em `CashSave/CashSave.py` e aparece somente em Preferências. A página `/assistente` usa o estado existente e seu `on_load` restaura o histórico persistido; a aplicação não expõe um sinal confiável de disponibilidade do modelo.

## Goals / Non-Goals

**Goals:**

- Adicionar um único ponto de acesso flutuante ao shell compartilhado, com visibilidade controlada pelo estado de autenticação e rota atual.
- Manter o atalho acessível por teclado e toque, com tooltip, animação CSS leve e suporte a movimento reduzido.
- Usar a rota e o fluxo de histórico já existentes, sem alterar a conversa.

**Non-Goals:**

- Criar painel, conversa, cópia de estado ou integração de IA paralela.
- Acrescentar um indicador de presença sem uma fonte de disponibilidade confiável.
- Redesenhar o menu lateral ou os formulários de Preferências.

## Decisions

1. **Renderizar o atalho em `app_layout`.** A função já centraliza a composição das páginas e recebe a rota ativa. O componente será condicionado a `AppState.autenticado` e omitido em `/assistente` e `/perfil`. Isso evita duplicação por página e reduz conflito com o chat e o formulário de Preferências. Um `z-index` abaixo das sobreposições do Radix mantém diálogos prioritários à frente.
2. **Navegar para `/assistente` em vez de montar um painel flutuante.** Não há um componente de painel de conversa compartilhável; montar outro chat duplicaria a interface e poderia disputar o estado e o histórico. A navegação existente aciona o carregamento e a restauração atuais, enquanto a transição da página usa a animação já presente no shell.
3. **Usar Reflex e CSS já disponíveis.** Um botão `rx.button` com ícone `bot`, nome acessível e `rx.tooltip` atenderá mouse, foco e leitores de tela. CSS em `cashsave-theme.css` controlará entrada, flutuação discreta, gradiente, hover e pressão. A regra global `prefers-reduced-motion` será preservada e complementada se necessário. Nenhuma dependência nova será adicionada.
4. **Não apresentar estado de disponibilidade.** Como o app não informa com confiabilidade se o Jarvis está pronto ou online, não será exibido indicador de presença.

## Risks / Trade-offs

- [O botão pode encobrir ações no canto inferior em telas pequenas] → manter dimensões e offsets responsivos com safe area, reservar espaço inferior no conteúdo e ocultá-lo nas rotas prioritárias.
- [Animação pode conflitar com preferência de movimento reduzido] → desativar animações e transições não essenciais sob `prefers-reduced-motion`.
- [Diálogo pode abrir próximo ao botão] → manter o botão abaixo da camada de diálogos e permitir que o overlay tome prioridade.

## Migration Plan

Não há migração de dados. Adicionar o componente ao shell, retirar sua instância local de Preferências e validar navegação, responsividade e acessibilidade. Para rollback, remover a integração do shell e os estilos novos; o menu existente para `/assistente` permanece disponível.
