// Proventos anunciados ou recebidos pertencentes ao usuário autenticado
table investimento_proventos {
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
      values = ["dividendo", "jcp", "rendimento_fii", "outro"]
    }
    enum status?=anunciado {
      values = ["anunciado", "pago"]
    }
    int valor_centavos filters=min:1
    decimal? quantidade_elegivel? filters=min:0
    date? data_anuncio?
    date? data_pagamento?
    text? observacoes? filters=trim
    timestamp criado_em?=now
    timestamp atualizado_em?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "usuario_id"}]}
    {type: "btree", field: [{name: "ativo_codigo"}]}
    {type: "btree", field: [{name: "status"}]}
    {
      type : "btree"
      field: [{name: "usuario_id"}, {name: "data_pagamento", op: "desc"}]
    }
  ]

  guid = "qEwfQFkZa0CMfNfJZFVvQ_Pw"
}
