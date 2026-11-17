// Ativos favoritos pertencentes ao usuário autenticado
table investimento_favoritos {
  auth = false

  schema {
    int id
    int usuario_id {
      table = "user"
    }

    text ativo_codigo filters=trim
    enum ativo_categoria {
      values = ["acao", "fii", "etf"]
    }
    timestamp criado_em?=now
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {
      type: "btree|unique"
      field: [{name: "usuario_id"}, {name: "ativo_codigo"}]
    }
    {type: "btree", field: [{name: "usuario_id"}]}
  ]

  guid = "9gDrtPq3_f2mZ7xkV1aN6cYbW8s"
}
