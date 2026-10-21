query "contas_a_pagar/pendentes" verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
  }

  stack {
    db.query contas_a_pagar {
      where = $db.contas_a_pagar.usuario_id == $auth.id && $db.contas_a_pagar.status == "pendente"
      return = {type: "list"}
    } as $contas
  }

  response = $contas
  guid = "fKfe9hYMTEBr4v05DCWuV9-421g"
}