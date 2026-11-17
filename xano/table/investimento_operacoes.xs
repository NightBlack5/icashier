// Operações de investimento pertencentes ao usuário autenticado
table investimento_operacoes {
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
    enum tipo {
      values = ["compra", "venda"]
    }
    date data
    decimal quantidade filters=min:0.0001
    int preco_unitario_centavos filters=min:1
    int custos_centavos?=0 filters=min:0
    text? observacoes? filters=trim
    timestamp criado_em?=now
    timestamp atualizado_em?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "usuario_id"}]}
    {type: "btree", field: [{name: "ativo_codigo"}]}
    {
      type : "btree"
      field: [{name: "usuario_id"}, {name: "ativo_codigo"}, {name: "data"}]
    }
  ]

  guid = "m7JP6za5xX5zNz6fB84Jq3sD"
}
