query contas verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
  }

  stack {
    db.query contas {
      where = $db.contas.usuario_id == $auth.id
      sort = {contas.nome: "asc"}
    } as $contas
  }

  response = $contas
  guid = "JiLc0aGkYZ6yH_X5hqYbGynWQGM"
}
