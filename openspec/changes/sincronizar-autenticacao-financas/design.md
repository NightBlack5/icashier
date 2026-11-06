# Design: sincronizar-autenticacao-financas

## Abordagem

Descrever os comportamentos que já aparecem nas alterações locais, separando os fluxos de conta dos dados e operações financeiras. Os artefatos são uma sincronização documental do estado atual do código, não uma declaração de que ele foi validado em produção.

## Conta e perfil

As páginas `/cadastro` e `/login` usam o estado Reflex para validar os campos, chamar as APIs de autenticação do Xano e manter o token da sessão. A foto do perfil é atualizada ou removida pelas rotas autenticadas de avatar.

No login, o e-mail é aparado e convertido para minúsculas; a senha é aparada e enviada como texto, sem hash no cliente. Campos vazios após a normalização impedem a chamada. A resposta precisa conter `authToken`; o usuário e o avatar retornados são armazenados no estado e a navegação segue para `/app`. Erros HTTP exibem a mensagem amigável do Xano quando disponível, e o estado de carregamento é encerrado em qualquer resultado.

## Finanças

A tela Finanças usa o endpoint autenticado `resumo` para carregar dados do usuário, transações, contas, categorias, contas a pagar, orçamentos, metas, recorrências e preferências. Filtros de transação e exportação CSV são processados no estado da aplicação.

Recorrências são armazenadas por usuário no Xano. Ao carregar os dados, o aplicativo processa ocorrências vencidas e avança a próxima data. O fluxo tem uma verificação de ocorrência duplicada. A interface detecta se o resumo inclui recorrências e informa quando os endpoints/tabelas ainda precisam ser publicados.

## Verificação pendente

Os artefatos não afirmam que as alterações Xano foram publicadas nem que os fluxos foram testados em navegador ou contra um workspace Xano. Essa validação deve ser realizada antes de arquivar a mudança.
