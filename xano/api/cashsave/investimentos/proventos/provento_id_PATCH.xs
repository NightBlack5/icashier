query "investimentos/proventos/{provento_id}" verb=PATCH {
  api_group = "cashsave"
  auth = "user"

  input {
    int provento_id
    text? ativo_codigo? filters=trim
    enum? ativo_categoria? {
      values = ["acao", "fii", "etf"]
    }
    enum? tipo? {
      values = ["dividendo", "jcp", "rendimento_fii", "outro"]
    }
    enum? status? {
      values = ["anunciado", "pago"]
    }
    int? valor_centavos? filters=min:1
    decimal? quantidade_elegivel? filters=min:0
    date? data_anuncio?
    date? data_pagamento?
    text? observacoes? filters=trim
  }

  stack {
    db.query investimento_proventos {
      where = $db.investimento_proventos.id == $input.provento_id && $db.investimento_proventos.usuario_id == $auth.id
      return = {type: "single"}
    } as $provento

    precondition ($provento != null) {
      error_type = "accessdenied"
      error = "Provento não encontrado."
    }

    var $status { value = $input.status ?? $provento.status }
    var $data_pagamento { value = $input.data_pagamento ?? $provento.data_pagamento }

    precondition ($status != "pago" || $data_pagamento != null) {
      error_type = "inputerror"
      error = "Informe a data de pagamento para um provento recebido."
    }

    db.edit investimento_proventos {
      field_name = "id"
      field_value = $provento.id
      data = {
        ativo_codigo: ($input.ativo_codigo|to_upper) ?? $provento.ativo_codigo
        ativo_categoria: $input.ativo_categoria ?? $provento.ativo_categoria
        tipo: $input.tipo ?? $provento.tipo
        status: $status
        valor_centavos: $input.valor_centavos ?? $provento.valor_centavos
        quantidade_elegivel: $input.quantidade_elegivel ?? $provento.quantidade_elegivel
        data_anuncio: $input.data_anuncio ?? $provento.data_anuncio
        data_pagamento: $data_pagamento
        observacoes: $input.observacoes ?? $provento.observacoes
        atualizado_em: now
      }
    } as $atualizado
  }

  response = $atualizado
  guid = "WQl8t8no9S6ktxh1hHjLG3EU"
}
