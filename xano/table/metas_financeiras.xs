// Metas financeiras e progresso de economia por usuário
table metas_financeiras {
  auth = false

  schema {
    int id
    int usuario_id {
      table = "user"
    }

    text nome filters=trim
    text? descricao? filters=trim
    int valor_objetivo_centavos filters=min:1
    int valor_atual_centavos? filters=min:0
    date? data_alvo?

    enum status?=ativa {
      values = ["ativa", "concluida", "arquivada"]
    }

    timestamp criado_em?=now
    timestamp atualizado_em?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "usuario_id"}]}
    {type: "btree", field: [{name: "status"}]}
    {type: "btree", field: [{name: "data_alvo"}]}
  ]

  guid = "ZkYIzfzVsWtzxEKW3pl6-Zg-EQ4"
}
