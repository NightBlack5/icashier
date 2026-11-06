# Habilitar upload de avatar

## Objetivo

Permitir que uma pessoa autenticada selecione e envie uma foto de perfil sem
que a ausência de `avatar_url` no resumo inicial desabilite o controle.

## Escopo

- Habilitar os controles de upload e remoção para sessões autenticadas.
- Manter validação de tipo, assinatura e tamanho do arquivo.
- Exibir o erro retornado pelo Xano quando as rotas de avatar não estiverem
  publicadas.

## Fora de escopo

- Criar ou alterar endpoints no Xano.
- Armazenar a imagem no navegador ou no servidor Reflex.
