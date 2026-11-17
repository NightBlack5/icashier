query "investimentos/favoritos" verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
  }

  stack {
    db.query investimento_favoritos {
      where = $db.investimento_favoritos.usuario_id == $auth.id
      sort = {investimento_favoritos.ativo_codigo: "asc"}
    } as $favoritos
  }

  response = $favoritos
  guid = "fAV0R1T0sG3tC4shS4v3"
}
