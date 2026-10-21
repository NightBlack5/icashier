# Persistir avatar público no Xano

## Objetivo

Fazer o endpoint de upload transformar o arquivo recebido em metadado de
imagem pública com URL, em vez de salvar diretamente o recurso temporário.

## Escopo

- Usar `storage.create_image` com acesso público.
- Salvar o metadado retornado no campo `avatar_url`.
- Publicar somente a rota POST de avatar após preview.

## Fora de escopo

- Alterar tabelas ou registros existentes.
- Tornar outros arquivos públicos.
