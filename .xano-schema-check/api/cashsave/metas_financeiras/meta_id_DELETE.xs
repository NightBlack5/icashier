query "metas_financeiras/{meta_id}" verb=DELETE {
  api_group = "cashsave"
  auth = "user"

  input {
    int meta_id
  }

  stack {
    db.query metas_financeiras {
      where = $db.metas_financeiras.id == $input.meta_id && $db.metas_financeiras.usuario_id == $auth.id
      return = {type: "single"}
    } as $meta
  
    precondition ($meta != null) {
      error_type = "accessdenied"
      error = "Meta financeira não encontrada."
    }
  
    db.del metas_financeiras {
      field_name = "id"
      field_value = $meta.id
    }
  }

  response = {success: true}
  guid = "CDBV75-te6n2kpnLxtdZunEbYsI"
}