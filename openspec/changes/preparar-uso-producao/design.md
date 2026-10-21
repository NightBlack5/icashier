# Design: preparar-uso-producao

## Abordagem

Manter o token na sessão existente do Reflex e usar esse mesmo valor para compor o cabeçalho Bearer consumido pelos endpoints Xano. Chamadas sem token continuam sem cabeçalho Authorization. Os testes exercitam a requisição criada, sem exibir o token nem acessar o serviço externo.

## Verificação

Testes unitários interceptam a criação da requisição para confirmar que o token é enviado como `Bearer <token>` e que chamadas sem token não enviam o cabeçalho. A verificação não acessa a rede nem depende de credenciais reais.

O perfil retornado pela API é JSON e pode conter um identificador numérico. O estado Reflex deve aceitar valores JSON no registro de usuário; as propriedades de nome, e-mail e avatar só expõem strings validadas à interface.

O Reflex oferece `rx.LocalStorage` como uma variável string. A lista de notificações dispensadas será serializada em JSON dentro dessa string e validada ao ser lida.

## Limite operacional

Este ajuste habilita as chamadas autenticadas no código, mas não prova que as alterações Xano locais estão publicadas nem substitui configuração de HTTPS e segredos na hospedagem de produção.
