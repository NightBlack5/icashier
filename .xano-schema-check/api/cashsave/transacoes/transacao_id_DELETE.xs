query "transacoes/{transacao_id}" verb=DELETE {
  api_group = "cashsave"
  auth = "user"

  input {
    int transacao_id
  }

  stack {
    db.query transacoes {
      where = $db.transacoes.id == $input.transacao_id && $db.transacoes.usuario_id == $auth.id
      return = {type: "single"}
    } as $transacao
  
    precondition ($transacao != null) {
      error_type = "accessdenied"
      error = "Transação não encontrada."
    }
  
    db.del transacoes {
      field_name = "id"
      field_value = $transacao.id
    }
  }

  response = {success: true}
  guid = "4v3cQ5EqCj2xinyQ1tnJghtqX7I"
}