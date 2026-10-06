// Query all cliente records
query cliente verb=GET {
  api_group = "Members & Accounts"

  input {
  }

  stack {
    db.query cliente {
      return = {type: "list"}
    } as $cliente
  }

  response = $cliente
  guid = "f3Z-g-Az39srxnxBeEtl8Dxvhas"
}