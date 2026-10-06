query transacoes verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
  }

  stack {
    db.query transacoes {
      where = $db.transacoes.usuario_id == $auth.id
      sort = {transacoes.data: "desc"}
    } as $transacoes
  }

  response = $transacoes
  guid = "kG8HzumqVtIbhM0DWWDy2lVXIUk"
}
