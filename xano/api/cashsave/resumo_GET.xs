query resumo verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "name", "email", "avatar_url"]
    } as $usuario

    db.query transacoes {
      where = $db.transacoes.usuario_id == $auth.id
      sort = {transacoes.data: "desc"}
    } as $transacoes

    db.query contas {
      where = $db.contas.usuario_id == $auth.id
      sort = {contas.nome: "asc"}
    } as $contas

    db.query categorias {
      where = $db.categorias.usuario_id == $auth.id || $db.categorias.usuario_id == null
      sort = {categorias.nome: "asc"}
    } as $categorias

    db.query contas_a_pagar {
      where = $db.contas_a_pagar.usuario_id == $auth.id
      sort = {contas_a_pagar.data_vencimento: "asc"}
    } as $contas_a_pagar

    db.query orcamentos {
      where = $db.orcamentos.usuario_id == $auth.id
      sort = {orcamentos.data_inicio: "desc"}
    } as $orcamentos

    db.query metas_financeiras {
      where = $db.metas_financeiras.usuario_id == $auth.id
      sort = {metas_financeiras.data_alvo: "asc"}
    } as $metas

    db.query recorrencias {
      where = $db.recorrencias.usuario_id == $auth.id
      sort = {recorrencias.proxima_data: "asc"}
    } as $recorrencias

    db.query preferencias_usuario {
      where = $db.preferencias_usuario.usuario_id == $auth.id
      return = {type: "single"}
    } as $preferencias
  }

  response = {
    usuario: $usuario
    transacoes: $transacoes
    contas: $contas
    categorias: $categorias
    contas_a_pagar: $contas_a_pagar
    orcamentos: $orcamentos
    metas: $metas
    recorrencias: $recorrencias
    preferencias: $preferencias
  }
  guid = "5ZzQxF7mlTD7QDjxbBGHv9Hr_-Q"
}
