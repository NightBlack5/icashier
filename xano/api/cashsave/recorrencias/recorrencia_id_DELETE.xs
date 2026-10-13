query "recorrencias/{recorrencia_id}" verb=DELETE {
  api_group = "cashsave"
  auth = "user"

  input {
    int recorrencia_id
  }

  stack {
    db.query recorrencias {
      where = $db.recorrencias.id == $input.recorrencia_id && $db.recorrencias.usuario_id == $auth.id
      return = {type: "single"}
    } as $recorrencia

    precondition ($recorrencia != null) {
      error_type = "accessdenied"
      error = "Recorrência não encontrada."
    }

    db.delete recorrencias {
      field_name = "id"
      field_value = $recorrencia.id
    } as $apagada
  }

  response = {success: true}
  guid = "a03214c9-0302-4a0a-9617-c37303489f30"
}
