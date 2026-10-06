query categorias verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
  }

  stack {
    db.query categorias {
      where = $db.categorias.usuario_id == $auth.id || $db.categorias.usuario_id == null
      sort = {categorias.nome: "asc"}
    } as $categorias
  }

  response = $categorias
  guid = "8nR33Ic-hufw9due00hlN2l7UFw"
}
