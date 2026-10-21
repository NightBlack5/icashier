// Add cliente record
query cliente verb=POST {
  api_group = "Members & Accounts"

  input {
    dblink {
      table = "cliente"
    }
  }

  stack {
    db.add cliente {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $cliente
  }

  response = $cliente
  guid = "nMI9bE_7WkGR65icbwpo9ZylHHs"
}