# Corrigir URL do avatar

## Objetivo

Aceitar os formatos de metadados de arquivo retornados pelo Xano para que o
avatar seja atualizado após um upload confirmado.

## Escopo

- Ler URL pública, assinada, de download ou link nos metadados.
- Cobrir objetos de arquivo aninhados.
- Manter falha explícita quando nenhuma URL utilizável for retornada.

## Fora de escopo

- Expor arquivos privados sem URL fornecida pelo Xano.
