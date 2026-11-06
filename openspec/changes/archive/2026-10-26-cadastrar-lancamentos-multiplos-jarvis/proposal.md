# Cadastro de múltiplos lançamentos pelo Jarvis

## Por que

Quando uma mensagem descreve receitas e várias despesas e pergunta pelos totais,
o parser atual escolhe um único tipo e o primeiro valor. Isso pode cadastrar uma
receita com a descrição de toda a mensagem e deixar de registrar as despesas ou
responder à pergunta.

## O que muda

- Interpretar cada valor e sua receita ou despesa separadamente em mensagens
  financeiras explícitas.
- Gravar cada lançamento confirmado pelo Xano e atualizar a lista local.
- Depois de todos os lançamentos serem confirmados, informar o total de receitas,
  o total de despesas e o saldo do conjunto informado.
- Informar claramente quando apenas parte dos lançamentos tiver sido confirmada.

## Capacidades

### Novas capacidades
- `assistant-batch-transactions`
- `assistant-quality`: confirmar operações financeiras somente após a confirmação do Xano.

### Capacidades modificadas
- Nenhuma.

## Fora do escopo

- Criar ou alterar categorias e contas automaticamente.
- Permitir que Ollama execute chamadas de API ou decida valores a gravar.
- Alterar registros financeiros já existentes.

## Impacto

- Parser local e estado do assistente em `CashSave/`.
- Testes automatizados do parser e do fluxo autenticado de gravação.
- A publicação do endpoint `transacoes` no Xano continua necessária para uso
  integrado.
