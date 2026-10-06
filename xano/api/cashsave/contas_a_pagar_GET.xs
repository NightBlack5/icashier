query contas_a_pagar verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
  }

  stack {
    db.query contas_a_pagar {
      where = $db.contas_a_pagar.usuario_id == $auth.id
      sort = {contas_a_pagar.data_vencimento: "asc"}
    } as $contas
  }

  response = $contas
  guid = "JM3tLI6lRMCzHOWeHtqdUs4MP9s"
}
