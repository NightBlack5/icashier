query "contas_a_pagar/{conta_a_pagar_id}" verb=DELETE {
  api_group = "cashsave"
  auth = "user"

  input {
    int conta_a_pagar_id
  }

  stack {
    db.query contas_a_pagar {
      where = $db.contas_a_pagar.id == $input.conta_a_pagar_id && $db.contas_a_pagar.usuario_id == $auth.id
      return = {type: "single"}
    } as $conta

    precondition ($conta != null) {
      error_type = "accessdenied"
      error = "Conta a pagar não encontrada."
    }

    db.del contas_a_pagar {
      field_name = "id"
      field_value = $conta.id
    }
  }

  response = {success: true}
  guid = "8gZzqt58TBEXeA1RzRX6d0aL6_M"
}
