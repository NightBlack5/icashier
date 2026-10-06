// Get cliente record
query "cliente/{cliente_id}" verb=GET {
  api_group = "Members & Accounts"

  input {
    int cliente_id? filters=min:1
  }

  stack {
    db.get cliente {
      field_name = "id"
      field_value = $input.cliente_id
    } as $cliente
  
    precondition ($cliente != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $cliente
  guid = "Cuwdp3H6ER7wLBHFdz3rvCJL5D4"
}