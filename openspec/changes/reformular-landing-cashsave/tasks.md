# Tasks

## 1. Composição da landing page

- [x] 1.1 Reformular hero, navegação fixa e dashboard ilustrativo com hierarquia visual responsiva.
- [x] 1.2 Apresentar Jarvis em uma demonstração de conversa estática e explicitamente ilustrativa.
- [x] 1.3 Criar seções distintas de recursos, como funciona, chamada final e rodapé com links existentes.

## 2. Movimento, acessibilidade e comportamento

- [x] 2.1 Adicionar animações CSS discretas e efeitos de interação sem novas dependências.
- [x] 2.2 Preservar suporte a `prefers-reduced-motion`, navegação por âncoras e foco visível.
- [x] 2.3 Confirmar que CTAs levam às rotas existentes de cadastro e acesso e que exemplos não alteram dados.

## 3. Validação

- [x] 3.1 Validar OpenSpec, compilação Reflex e testes relevantes.
- [x] 3.2 Revisar no navegador em desktop e mobile; verificar seções, links, console e movimento reduzido.

## Observação de validação

O navegador integrado exibiu as páginas e concluiu a navegação para `/login`,
`/cadastro` e âncoras internas. Também registrou falhas de conexão WebSocket
local em `/_event`; a validação de rotas e conteúdo não dependeu dessa conexão,
e nenhum formulário foi enviado.
