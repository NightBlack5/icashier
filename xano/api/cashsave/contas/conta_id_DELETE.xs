query "contas/{conta_id}" verb=DELETE {
  api_group = "cashsave"
  auth = "user"

  input {
    int conta_id
  }

  stack {
    db.query contas {
      where = $db.contas.id == $input.conta_id && $db.contas.usuario_id == $auth.id
      return = {type: "single"}
    } as $conta

    precondition ($conta != null) {
      error_type = "accessdenied"
      error = "Conta não encontrada."
    }

    db.edit contas {
      field_name = "id"
      field_value = $conta.id
      data = {ativa: false}
    }
  }

  response = {success: true}
  guid = "1y4wWHemc9DoaRUWA6n01pzSVho"
}
