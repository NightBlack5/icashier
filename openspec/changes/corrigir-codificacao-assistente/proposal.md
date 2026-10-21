# Corrigir codificação da assistente

## Objetivo

Corrigir textos em português exibidos com mojibake na assistente e preservar
acentos em mensagens do estado Reflex.

## Escopo

- Reparar textos corrompidos em `state.py`.
- Adicionar regressão para detectar marcadores de dupla codificação.
- Validar compilação e testes.

## Fora de escopo

- Alterar o modelo Ollama ou as regras financeiras.
