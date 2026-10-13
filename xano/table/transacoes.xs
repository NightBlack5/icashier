// Transacoes financeiras de receitas e despesas do usuario
table transacoes {
  auth = false

  schema {
    int id
    int usuario_id {
      table = "user"
    }

    int? conta_id? {
      table = "contas"
    }

    int? categoria_id? {
      table = "categorias"
    }

    int? recorrencia_id?

    enum tipo {
      values = ["receita", "despesa"]
    }

    text descricao filters=trim
    int valor_centavos filters=min:1
    date data
    date? recorrencia_data?
    text? observacoes? filters=trim
    timestamp criado_em?=now
    timestamp atualizado_em?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "usuario_id"}]}
    {type: "btree", field: [{name: "conta_id"}]}
    {type: "btree", field: [{name: "categoria_id"}]}
    {type: "btree", field: [{name: "tipo"}]}
    {type: "btree", field: [{name: "data", op: "desc"}]}
    {
      type : "btree"
      field: [{name: "usuario_id"}, {name: "data", op: "desc"}]
    }
    {
      type : "btree|unique"
      field: [{name: "recorrencia_id"}, {name: "recorrencia_data"}]
    }
  ]

  guid = "Em9Mx_6510JzKQuBO6QQOdlNod4"
}
