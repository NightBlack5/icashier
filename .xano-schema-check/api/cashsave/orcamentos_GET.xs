query orcamentos verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
  }

  stack {
    db.query orcamentos {
      where = $db.orcamentos.usuario_id == $auth.id
      return = {type: "list"}
    } as $orcamentos
  }

  response = $orcamentos
  guid = "Z1M9vaSVDg-39rjXi9Wc5eifhME"
}