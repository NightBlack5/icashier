// Delete cliente record.
query "cliente/{cliente_id}" verb=DELETE {
  api_group = "Members & Accounts"

  input {
    int cliente_id? filters=min:1
  }

  stack {
    db.del cliente {
      field_name = "id"
      field_value = $input.cliente_id
    }
  }

  response = null
  guid = "0E7TuP9S-MyUfgtGjWxd3uC_KdI"
}