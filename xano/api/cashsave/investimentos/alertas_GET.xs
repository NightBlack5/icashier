query "investimentos/alertas" verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
  }

  stack {
    db.query investimento_alertas {
      where = $db.investimento_alertas.usuario_id == $auth.id
      sort = {investimento_alertas.criado_em: "desc"}
    } as $alertas
  }

  response = $alertas
  guid = "4l3rt5C4shS4v3G3t"
}
