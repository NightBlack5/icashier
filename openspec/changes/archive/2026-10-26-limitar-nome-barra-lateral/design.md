# Design

## Context

Os textos já possuem `overflow`, `text_overflow` e `white_space`, mas os contêineres flexíveis não reservam explicitamente espaço mínimo zero. Em flex layout, isso permite que o item preserve a largura intrínseca do nome.

## Goals / Non-Goals

**Goals:**

- Fazer o bloco do nome ocupar somente o espaço restante após avatar e espaçamento.
- Aplicar truncamento de forma consistente nas três barras laterais.

**Non-Goals:**

- Alterar o nome salvo do usuário ou a largura geral da navegação.

## Decisions

- Definir `width="0"`, `min_width="0"` e `flex="1"` no contêiner do nome.
- Adicionar `title` ao texto para preservar acesso ao nome completo sem aumentar o layout.

## Risks / Trade-offs

- [Risco] O título depende do suporte do navegador. -> Mitigação: o texto acessível continua presente no elemento e a abreviação visual é apenas de layout.
