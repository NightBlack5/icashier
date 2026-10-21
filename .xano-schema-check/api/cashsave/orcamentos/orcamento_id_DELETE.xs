query "orcamentos/{orcamento_id}" verb=DELETE {
  api_group = "cashsave"
  auth = "user"

  input {
    int orcamento_id
  }

  stack {
    db.query orcamentos {
      where = $db.orcamentos.id == $input.orcamento_id && $db.orcamentos.usuario_id == $auth.id
      return = {type: "single"}
    } as $orcamento
  
    precondition ($orcamento != null) {
      error_type = "accessdenied"
      error = "Orçamento não encontrado."
    }
  
    db.del orcamentos {
      field_name = "id"
      field_value = $orcamento.id
    }
  }

  response = {success: true}
  guid = "5hPi6a-f6euEBgB7QXQ8mNWIbpg"
}