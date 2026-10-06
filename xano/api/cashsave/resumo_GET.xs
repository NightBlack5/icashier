query resumo verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
  }

  stack {
    db.query transacoes {
      where = $db.transacoes.usuario_id == $auth.id
      sort = {transacoes.data: "desc"}
    } as $transacoes

    db.query contas_a_pagar {
      where = $db.contas_a_pagar.usuario_id == $auth.id && $db.contas_a_pagar.status == "pendente"
      sort = {contas_a_pagar.data_vencimento: "asc"}
    } as $contas_pendentes
  }

  response = {
    transacoes: $transacoes
    contas_pendentes: $contas_pendentes
  }
  guid = "5ZzQxF7mlTD7QDjxbBGHv9Hr_-Q"
}
