# Proposal

## Why

O projeto possui uma apresentação visual anterior, mas ainda não existe um
case study orientado a recrutadores que explique, com evidências reais, o
produto, a arquitetura, as decisões técnicas e os limites atuais do CashSave.
Este material transforma o projeto em uma peça de portfólio profissional sem
apresentar fluxos autenticados não verificados como concluídos.

## What Changes

- Criar `portfolio/APRESENTACAO_PROJETO.html` como fonte editorial do PDF.
- Criar `portfolio/APRESENTACAO_PROJETO.pdf` em formato A4 horizontal, com
  identidade visual consistente, capa, narrativa do produto, galeria, stack,
  arquitetura, desafios, UX, resultado e campos editáveis do desenvolvedor.
- Copiar para `portfolio/assets/` somente capturas reais e diagramas gerados
  para o documento.
- Distinguir visualmente comportamento verificado, dependências externas e
  próximos passos.
- Validar que o PDF tem texto pesquisável, imagens incorporadas, páginas
  renderizáveis e nenhum caminho de asset quebrado.

## Capabilities

### New Capabilities

- `professional-project-portfolio`: apresentação estática e verificável do
  projeto CashSave para avaliação profissional.

### Modified Capabilities

Nenhuma.

## Impact

- Afeta somente `portfolio/` e os artefatos de planejamento deste change.
- Não altera o aplicativo, APIs, banco, dependências ou comportamento de
  runtime.
- A geração usa HTML/CSS e Chromium local; as imagens são derivadas das
  capturas existentes do runtime.
