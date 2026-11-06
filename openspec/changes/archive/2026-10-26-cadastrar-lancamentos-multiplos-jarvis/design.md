# Design

## Contexto

O fluxo atual reconhece uma única intenção e extrai somente o primeiro valor da
mensagem. Uma frase com salário, despesas e uma pergunta termina no ramo de
gravação e a descrição da primeira transação absorve o restante do texto.

## Decisões

- Um parser determinístico local extrai todos os valores monetários e associa
  cada um ao tipo de transação declarado mais recentemente na mesma frase.
- O parser valida todos os valores e descrições antes de iniciar qualquer
  gravação. Perguntas que começam como consulta continuam no fluxo de análise e
  não são convertidas em lançamentos.
- Cada transação usa o endpoint autenticado `POST transacoes`. A aplicação só
  atualiza o estado local após receber uma resposta com `id`.
- Totais e saldo são calculados em centavos exclusivamente a partir dos
  lançamentos da mensagem. A resposta identifica que o saldo se refere ao
  conjunto informado, não ao saldo global da conta.
- Se uma gravação falhar após outras serem confirmadas, o Jarvis informa quantas
  foram salvas e qual lançamento falhou; não declara o lote completo como
  sucesso.
- Categoria e conta só são associadas quando resolvidas pelos dados carregados
  do usuário; o parser não cria registros auxiliares nem inventa IDs.

## Riscos

- Uma mensagem extensa pode conter valores que não sejam transações. A extração
  exige uma intenção financeira reconhecida antes de cada valor e limita o texto
  descritivo à frase/trecho correspondente.
- O endpoint não oferece transação atômica para um lote. Uma falha remota pode
  deixar gravações parciais, que serão reportadas explicitamente.

## Verificação

- Testar a mensagem de salário e cinco despesas, incluindo valores brasileiros,
  tipos, descrições e o resultado de R$ 680,00.
- Testar validação anterior à escrita, confirmação após resposta do Xano e falha
  parcial.
- Executar a suíte offline, a compilação Reflex e `openspec validate`.
