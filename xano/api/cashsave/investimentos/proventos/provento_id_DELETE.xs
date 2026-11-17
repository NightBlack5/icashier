query "investimentos/proventos/{provento_id}" verb=DELETE {
  api_group = "cashsave"
  auth = "user"

  input {
    int provento_id
  }

  stack {
    db.query investimento_proventos {
      where = $db.investimento_proventos.id == $input.provento_id && $db.investimento_proventos.usuario_id == $auth.id
      return = {type: "single"}
    } as $provento

    precondition ($provento != null) {
      error_type = "accessdenied"
      error = "Provento não encontrado."
    }

    db.del investimento_proventos {
      field_name = "id"
      field_value = $provento.id
    }
  }

  response = {success: true}
  guid = "yr5t47Rwoan3GJwlxTd0Zc5W"
}
