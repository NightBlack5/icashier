// Categorias financeiras de receitas e despesas
table categorias {
  auth = false

  schema {
    int id
    int? usuario_id? {
      table = "user"
    }
  
    text nome filters=trim
    enum tipo {
      values = ["receita", "despesa"]
    }
  
    text? icone? filters=trim
    text? cor? filters=trim
    bool criada_pelo_usuario?
    timestamp criada_em?=now
    timestamp atualizada_em?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "usuario_id"}]}
    {type: "btree", field: [{name: "tipo"}]}
    {
      type : "btree"
      field: [{name: "usuario_id"}, {name: "tipo"}]
    }
  ]

  guid = "oIw84ybN2P3GxO4FH5fGiHBiOE8"
  items = []
}