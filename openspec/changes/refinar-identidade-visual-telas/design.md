# Design: identidade visual premium

## Direção

Preservar o tema escuro e a identidade verde do CashSave. Usar fundos em
grafite-esmeralda, superfícies em camadas, verde luminoso somente para ações e
estados positivos, bordas sutis, contraste legível e sombras discretas. A
experiência deve continuar leve em telas pequenas e respeitar a preferência de
movimento reduzido do sistema.

## Implementação

- Centralizar cores, tipografia, foco, controles, scrollbar e movimento numa
  folha de estilos do app, sem adicionar dependências.
- Usar a folha nas rotas públicas e autenticadas e harmonizar o shell lateral,
  formulários, cards e páginas para compartilhar a mesma linguagem.
- Preservar os componentes Reflex, rotas, conteúdo dinâmico, acessibilidade e
  eventos existentes; manter leiaute fluido nos breakpoints atuais.
- Não usar recursos externos, não requerer serviços remotos e não substituir
  valores financeiros ou ações por conteúdo ilustrativo.

## Verificação

- Executar a suíte de testes e a compilação Reflex.
- Validar a mudança OpenSpec.
- Conferir as telas públicas e autenticadas no navegador quando o runtime local
  permitir; documentar telas que precisem de autenticação ou serviços externos.
