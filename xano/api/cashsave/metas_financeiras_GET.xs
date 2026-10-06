query metas_financeiras verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
  }

  stack {
    db.query metas_financeiras {
      where = $db.metas_financeiras.usuario_id == $auth.id
      sort = {metas_financeiras.data_alvo: "asc"}
    } as $metas
  }

  response = $metas
  guid = "LVUHtpW8bxujtT1W5KqOCYTQ3jg"
}
