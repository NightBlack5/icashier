query recorrencias verb=POST {
  api_group = "cashsave"
  auth = "user"

  input {
    int? conta_id?
    int? categoria_id?
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
  }

  stack {
    precondition ($input.descricao != "") {
      error_type = "inputerror"
      error = "Informe uma descrição para a recorrência."
    }

    db.add recorrencias {
      data = {
        usuario_id: $auth.id
        conta_id: $input.conta_id
        categoria_id: $input.categoria_id
        tipo: $input.tipo
        descricao: $input.descricao
        valor_centavos: $input.valor_centavos
        frequencia: $input.frequencia
        proxima_data: $input.proxima_data
        dia_referencia: $input.dia_referencia
        mes_referencia: $input.mes_referencia
        ativa: true
      }
    } as $recorrencia
  }

  response = $recorrencia
  guid = "ea99f9e8-01b4-429f-98a4-28e81591c092"
}
