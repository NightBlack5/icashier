// Agendamentos de receitas e despesas recorrentes por usuário
table recorrencias {
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
    enum frequencia {
      values = ["diaria", "semanal", "mensal", "anual"]
    }
    date proxima_data
    int dia_referencia filters=min:1|max:31
    int mes_referencia filters=min:1|max:12
    bool ativa?=true
    timestamp criado_em?=now
    timestamp atualizado_em?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "usuario_id"}]}
    {type: "btree", field: [{name: "ativa"}]}
    {type: "btree", field: [{name: "proxima_data"}]}
  ]

  guid = "3c6ae5e5-fd6a-45e8-96d3-3bf4482bb485"
}
