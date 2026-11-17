# Tasks

## 1. Integração no shell autenticado

- [x] 1.1 Compartilhar o atalho no shell das telas autenticadas, ocultando-o em `/assistente`, `/perfil` e quando não autenticado; validar as rotas elegíveis e prioritárias com testes focados.
- [x] 1.2 Remover a instância antiga de Preferências e direcionar o novo botão a `/assistente`; verificar que há um só atalho e que a restauração do histórico existente continua coberta pelos testes do Jarvis.

## 2. Apresentação, acessibilidade e responsividade

- [x] 2.1 Estilizar botão circular, tooltip, entrada, flutuação sutil, brilho, hover e pressão; verificar contraste, área de toque, foco de teclado e ausência de indicador online sem fonte confiável.
- [x] 2.2 Ajustar posição para desktop e mobile, reservar espaço contra sobreposição e respeitar `prefers-reduced-motion`; verificar 320 px, 390 px, tablet e desktop sem overflow ou animação contínua sob movimento reduzido.

## 3. Validação de integração

- [x] 3.1 Executar `reflex compile --dry`, os testes focados e `openspec validate botao-flutuante-jarvis`; corrigir falhas antes de concluir.
- [ ] 3.2 No navegador, verificar visibilidade após autenticação, tooltip e foco, navegação ao Jarvis com conversa existente, ausência nas telas prioritárias e prioridade de diálogos.

### Bloqueio da validação E2E

A rota `/perfil` redirecionou para login no navegador compartilhado e a conexão
WebSocket local do Reflex falhou. Sem uma sessão autenticada funcional, a
verificação visual do atalho dentro do aplicativo permanece pendente; nenhuma
credencial foi fornecida ou simulada.
