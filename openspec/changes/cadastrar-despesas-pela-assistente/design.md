# Design

O parser local identifica verbos de lançamento, um valor em reais e o texto
descritivo. A categoria e a conta são resolvidas por comparação exata ou
parcial com os registros já carregados para o usuário. Se não houver uma
categoria inequívoca, o cadastro é recusado e a pessoa é orientada a informar
uma categoria existente.

O estado Reflex monta o mesmo payload usado pelo cadastro manual e chama
`POST /transacoes` através de `_api`, que inclui o token da sessão. Somente
depois de uma resposta contendo `id` a transação é inserida no estado local.
O formulário atual continua usando `on_submit`, portanto Enter e o botão de
avião compartilham o mesmo evento.
