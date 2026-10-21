# Proposta: preparar-uso-producao

## Por que

O app depende do cabeçalho de autorização Bearer para acessar os endpoints protegidos do Xano. Esse contrato precisa ser confirmado por teste automatizado para evitar regressões que só aparecem após o login.

## O que muda

- Registrar como requisito o envio do token de sessão no cabeçalho Authorization.
- Cobrir chamadas com e sem token com testes automatizados.
- Aceitar com segurança os tipos JSON retornados para o perfil autenticado, incluindo IDs numéricos.
- Armazenar preferências locais de notificações no formato string suportado pelo Reflex.

## Fora do escopo

- Publicar alterações no workspace Xano.
- Implantar o app em um serviço de hospedagem ou configurar domínio/segredos de produção.

## Impacto

- Camada de comunicação entre `CashSave/state.py` e as APIs Xano.
- Testes automatizados para o contrato de autorização da credencial de sessão.
