query "investimentos/operacoes" verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
  }

  stack {
    db.query investimento_operacoes {
      where = $db.investimento_operacoes.usuario_id == $auth.id
      sort = {investimento_operacoes.data: "desc"}
    } as $operacoes
  }

  response = $operacoes
  guid = "BqC29ExBaQYKd3GD_2svLzCv"
}
