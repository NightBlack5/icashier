// Condições de alerta de investimento sem alegação de monitoramento ativo
table investimento_alertas {
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
    enum condicao {
      values = [
        "preco_acima",
        "preco_abaixo",
        "variacao_diaria_acima",
        "variacao_diaria_abaixo"
      ]
    }
    int? preco_limite_centavos? filters=min:1
    decimal? variacao_limite_percentual? filters=min:0.0001
    enum monitoramento_status?=nao_monitorado {
      values = ["nao_monitorado", "monitorado"]
    }
    bool ativo?=true
    timestamp criado_em?=now
    timestamp atualizado_em?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "usuario_id"}]}
    {type: "btree", field: [{name: "ativo_codigo"}]}
  ]

  guid = "4l3rt5C4shS4v3B0l54"
}
