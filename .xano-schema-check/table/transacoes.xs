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
  
    enum tipo {
      values = ["receita", "despesa"]
    }
  
    text descricao filters=trim
    int valor_centavos filters=min:1
    date data
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
  ]

  guid = "Em9Mx_6510JzKQuBO6QQOdlNod4"
  items = [
    {
      id            : 3
      usuario_id    : 3
      conta_id      : null
      categoria_id  : null
      tipo          : "despesa"
      descricao     : "Conta do Mercado primeiro mes"
      valor_centavos: 67787700
      data          : "2026-10-06"
      observacoes   : null
      criado_em     : 1791323599634
      atualizado_em : 0
    }
  ]
}