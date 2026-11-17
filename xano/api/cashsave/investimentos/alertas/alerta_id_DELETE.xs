query "investimentos/alertas/{alerta_id}" verb=DELETE {
  api_group = "cashsave"
  auth = "user"

  input {
    int alerta_id
  }

  stack {
    db.query investimento_alertas {
      where = $db.investimento_alertas.id == $input.alerta_id && $db.investimento_alertas.usuario_id == $auth.id
      return = {type: "single"}
    } as $alerta

    precondition ($alerta != null) {
      error_type = "accessdenied"
      error = "Alerta não encontrado."
    }

    db.del investimento_alertas {
      field_name = "id"
      field_value = $alerta.id
    }
  }

  response = {success: true}
  guid = "4l3rt5C4shS4v3D3l"
}
