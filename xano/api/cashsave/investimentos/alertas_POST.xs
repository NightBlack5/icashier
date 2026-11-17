query "investimentos/alertas" verb=POST {
  api_group = "cashsave"
  auth = "user"

  input {
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
  }

  stack {
    precondition ($input.ativo_codigo != "") {
      error_type = "inputerror"
      error = "Informe o código do ativo."
    }

    var $preco_valido {
      value = $input.preco_limite_centavos != null && ($input.condicao == "preco_acima" || $input.condicao == "preco_abaixo")
    }

    var $variacao_valida {
      value = $input.variacao_limite_percentual != null && ($input.condicao == "variacao_diaria_acima" || $input.condicao == "variacao_diaria_abaixo")
    }

    precondition ($preco_valido || $variacao_valida) {
      error_type = "inputerror"
      error = "Informe o limite correspondente à condição do alerta."
    }

    db.add investimento_alertas {
      data = {
        usuario_id: $auth.id
        ativo_codigo: $input.ativo_codigo|to_upper
        ativo_categoria: $input.ativo_categoria
        condicao: $input.condicao
        preco_limite_centavos: $input.preco_limite_centavos
        variacao_limite_percentual: $input.variacao_limite_percentual
        monitoramento_status: "nao_monitorado"
        ativo: true
      }
    } as $alerta
  }

  response = $alerta
  guid = "4l3rt5C4shS4v3P0st"
}
