query "investimentos/favoritos/{ativo_codigo}" verb=DELETE {
  api_group = "cashsave"
  auth = "user"

  input {
    text ativo_codigo filters=trim
  }

  stack {
    db.query investimento_favoritos {
      where = $db.investimento_favoritos.usuario_id == $auth.id && $db.investimento_favoritos.ativo_codigo == ($input.ativo_codigo|to_upper)
      return = {type: "single"}
    } as $favorito

    precondition ($favorito != null) {
      error_type = "accessdenied"
      error = "Favorito não encontrado."
    }

    db.del investimento_favoritos {
      field_name = "id"
      field_value = $favorito.id
    }
  }

  response = {success: true}
  guid = "fAV0R1T0sD3L3t3C4shS4v3"
}
