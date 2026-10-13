query recorrencias verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
  }

  stack {
    db.query recorrencias {
      where = $db.recorrencias.usuario_id == $auth.id
      sort = {recorrencias.proxima_data: "asc"}
    } as $recorrencias
  }

  response = $recorrencias
  guid = "7fa6ee7f-9472-46d1-8e50-6de34c852dd1"
}
