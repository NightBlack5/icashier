# Cadastro de despesas pela assistente

## Objetivo

Permitir que a assistente interprete comandos claros de cadastro de despesas e
grave a transação autenticada no Xano, mantendo o envio por Enter.

## Escopo

- Detectar localmente comandos de despesa com valor e descrição.
- Resolver categoria e conta somente entre os registros já carregados do usuário.
- Reutilizar o endpoint autenticado `POST /transacoes`.
- Atualizar a lista local após confirmação do Xano e informar erros explicitamente.
- Manter perguntas financeiras e respostas educativas existentes.

## Segurança e limites

- O Ollama não recebe permissão para chamar APIs, executar código ou alterar dados.
- Mensagens ambíguas ou sem valor válido não serão gravadas.
- A gravação usa exclusivamente o usuário autenticado e o endpoint existente.
- A primeira versão não editará nem excluirá registros.

## Fora de escopo

- Cadastro automático de categorias, contas ou receitas.
- Confirmação por botão ou alterações no esquema do Xano.
