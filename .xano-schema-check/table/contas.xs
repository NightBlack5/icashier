// Contas bancarias e carteiras financeiras do usuario
table contas {
  auth = false

  schema {
    int id
    int usuario_id {
      table = "user"
    }
  
    text nome filters=trim
    enum tipo {
      values = [
        "conta_corrente"
        "poupanca"
        "carteira"
        "cartao_credito"
        "outro"
      ]
    }
  
    text? instituicao? filters=trim
    int saldo_inicial_centavos?
    bool ativa?=true
    timestamp criado_em?=now
    timestamp atualizado_em?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "usuario_id"}]}
    {
      type : "btree"
      field: [{name: "usuario_id"}, {name: "ativa"}]
    }
  ]

  guid = "se4fUbHIuLfNfErzA41Q0YVDC38"
  items = []
}