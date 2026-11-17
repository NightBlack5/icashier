query "investimentos/proventos" verb=POST {
  api_group = "cashsave"
  auth = "user"

  input {
    text ativo_codigo filters=trim
    enum ativo_categoria {
      values = ["acao", "fii", "etf"]
    }
    enum tipo {
      values = ["dividendo", "jcp", "rendimento_fii", "outro"]
    }
    enum? status?=anunciado {
      values = ["anunciado", "pago"]
    }
    int valor_centavos filters=min:1
    decimal? quantidade_elegivel? filters=min:0
    date? data_anuncio?
    date? data_pagamento?
    text? observacoes? filters=trim
  }

  stack {
    precondition ($input.ativo_codigo != "") {
      error_type = "inputerror"
      error = "Informe o código do ativo."
    }

    precondition (
      $input.status != "pago" || $input.data_pagamento != null
    ) {
      error_type = "inputerror"
      error = "Informe a data de pagamento para um provento recebido."
    }

    db.add investimento_proventos {
      data = {
        usuario_id: $auth.id
        ativo_codigo: $input.ativo_codigo|to_upper
        ativo_categoria: $input.ativo_categoria
        tipo: $input.tipo
        status: $input.status ?? "anunciado"
        valor_centavos: $input.valor_centavos
        quantidade_elegivel: $input.quantidade_elegivel
        data_anuncio: $input.data_anuncio
        data_pagamento: $input.data_pagamento
        observacoes: $input.observacoes
      }
    } as $provento
  }

  response = $provento
  guid = "3x7yu2stDD6FqoAxFwN10CB0"
}
