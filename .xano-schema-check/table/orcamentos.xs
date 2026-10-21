// Orçamentos por usuário e período, com escopo opcional por categoria
table orcamentos {
  auth = false

  schema {
    int id
    int usuario_id {
      table = "user"
    }
  
    text nome filters=trim
    int? categoria_id? {
      table = "categorias"
    }
  
    int limite_centavos filters=min:1
    enum periodicidade {
      values = ["semanal", "mensal", "trimestral", "anual", "personalizada"]
    }
  
    date data_inicio
    date data_fim
    bool ativo?=true
    timestamp criado_em?=now
    timestamp atualizado_em?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "usuario_id"}]}
    {type: "btree", field: [{name: "data_inicio"}]}
    {type: "btree", field: [{name: "data_fim"}]}
  ]

  guid = "dJ5VPhn1RR6zKDTw31Xpz1oD0jo"
  items = []
}