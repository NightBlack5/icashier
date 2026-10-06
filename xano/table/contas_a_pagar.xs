// Contas a pagar e compromissos financeiros do usuario
table contas_a_pagar {
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

    text descricao filters=trim
    int valor_centavos filters=min:1
    date data_vencimento
    enum status?=pendente {
      values = ["pendente", "paga", "cancelada"]
    }

    date? data_pagamento?
    enum recorrencia?=nenhuma {
      values = ["nenhuma", "semanal", "mensal", "anual"]
    }

    text? observacoes? filters=trim
    timestamp criado_em?=now
    timestamp atualizado_em?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "usuario_id"}]}
    {
      type : "btree"
      field: [{name: "data_vencimento", op: "asc"}]
    }
    {type: "btree", field: [{name: "status"}]}
    {type: "btree", field: [{name: "conta_id"}]}
    {type: "btree", field: [{name: "categoria_id"}]}
    {
      type : "btree"
      field: [{name: "usuario_id"}, {name: "status"}]
    }
    {
      type : "btree"
      field: [{name: "usuario_id"}, {name: "data_vencimento", op: "asc"}]
    }
  ]

  guid = "BZf4skCWvmzfsm-21081n_wPKeg"
}
