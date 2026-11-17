# Design

## Contexto

A página `/` é composta em `CashSave/pages/landing.py`, e a folha global
`assets/cashsave-theme.css` já define tokens, identidade escura/verde e suporte
global a `prefers-reduced-motion`. O cadastro e o login são rotas Reflex
existentes (`/cadastro` e `/login`). A aplicação já apresenta finanças,
contas, metas, gráficos/resumos, perfil de investidor e o Jarvis. Não há
biblioteca de animação dedicada instalada.

## Objetivos

- Criar uma apresentação de produto premium e coerente com a identidade
  existente, mantendo componentes em Reflex e estilos no CSS local.
- Deixar claras as ações para cadastro/acesso e manter a navegação entre
  seções utilizável por mouse, teclado e toque.
- Mostrar apenas recursos existentes; rotular valores e conteúdo de demonstração
  como ilustrativos.
- Manter a conversa de demonstração do Jarvis inteiramente visual e isolada de
  qualquer estado, chamada de API ou transação real.
- Respeitar telas estreitas, reduzir movimento para quem assim preferir e
  evitar dependências externas.

## Não objetivos

- Mudar autenticação, fluxo de cadastro, lógica financeira ou a experiência do
  dashboard.
- Acrescentar uma segunda integração de IA ou fazer recomendações financeiras.
- Inventar estatísticas, certificações, garantias, políticas ou páginas
  institucionais não presentes no projeto.

## Decisões

1. **Componentes locais e CSS.** Reorganizar a composição no módulo da landing
   page e acrescentar classes específicas à folha de tema existente. Usar SVG
   inline e componentes Reflex para gráfico, cartões e ícones; não adicionar
   dependências ou imagens aleatórias.
2. **Rotas funcionais.** CTAs de cadastro apontam a `/cadastro`; acesso aponta
   a `/login`; links internos usam IDs estáveis de seção. O cabeçalho permanece
   visível durante a rolagem sem cobrir destinos de âncora.
3. **Demonstrações explicitamente ilustrativas.** O dashboard usa valores
   claramente marcados como exemplo e a conversa Jarvis é conteúdo estático,
   sem estado ou handlers financeiros.
4. **Animação progressiva e acessível.** Usar transformações/opacidade e
   animações CSS lentas e não essenciais ao conteúdo. Desativá-las em
   `prefers-reduced-motion`; evitar tarefas de animação JavaScript e depender
   de animações de rolagem experimentais para revelar conteúdo.
5. **Precisão de produto.** Recursos de finanças, contas, metas, gráficos,
   assistente e perfil são descritos conforme as telas existentes. O rodapé
   terá links disponíveis no produto, sem criar destinos de privacidade/termos
   ausentes.

## Riscos e mitigação

- **A tela pequena fica comprimida pela demonstração visual** → trocar
  sobreposições por empilhamento, limitar larguras e revisar no navegador em
  viewport mobile.
- **A animação prejudica leitura ou acessibilidade** → manter textos estáticos
  legíveis, usar apenas movimento decorativo e validar o modo reduced motion.
- **Exemplos confundidos com dados reais** → apresentar rótulo explícito no
  dashboard e na conversa.
- **Mudanças nos CTAs quebram o acesso** → testar diretamente os destinos
  `/cadastro` e `/login` no navegador sem submeter formulários.

## Plano de validação

Executar `openspec validate reformular-landing-cashsave`, compilar o app e rodar
os testes focados existentes. Abrir a página no navegador em desktop e largura
mobile; conferir todas as seções, console, âncoras e destinos de login/cadastro.
Validar a renderização com movimento reduzido e confirmar que a demonstração
Jarvis não produz mutações.
