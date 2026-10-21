# Upload automático de avatar

## Objetivo

Enviar a foto de perfil assim que um arquivo válido for selecionado no
componente de upload, sem exigir um segundo clique.

## Escopo

- Usar o evento `on_drop` do componente Reflex.
- Manter o botão de reenvio para repetir o upload se necessário.
- Exibir o nome do arquivo selecionado e erros reais do backend.

## Fora de escopo

- Alterar o endpoint Xano ou armazenar a imagem localmente.
