query "recorrencias/{recorrencia_id}" verb=PATCH {
  api_group = "cashsave"
  auth = "user"

  input {
    int recorrencia_id
    int? conta_id?
    int? categoria_id?
    enum? tipo? {
      values = ["receita", "despesa"]
    }
    text? descricao? filters=trim
    int? valor_centavos? filters=min:1
    enum? frequencia? {
      values = ["diaria", "semanal", "mensal", "anual"]
    }
    date? proxima_data?
    int? dia_referencia? filters=min:1|max:31
    int? mes_referencia? filters=min:1|max:12
    bool? ativa?
  }

  stack {
    db.query recorrencias {
      where = $db.recorrencias.id == $input.recorrencia_id && $db.recorrencias.usuario_id == $auth.id
      return = {type: "single"}
    } as $recorrencia

    precondition ($recorrencia != null) {
      error_type = "accessdenied"
      error = "Recorrência não encontrada."
    }

    db.edit recorrencias {
      field_name = "id"
      field_value = $recorrencia.id
      data = {
        conta_id: $input.conta_id ?? $recorrencia.conta_id
        categoria_id: $input.categoria_id ?? $recorrencia.categoria_id
        tipo: $input.tipo ?? $recorrencia.tipo
        descricao: $input.descricao ?? $recorrencia.descricao
        valor_centavos: $input.valor_centavos ?? $recorrencia.valor_centavos
        frequencia: $input.frequencia ?? $recorrencia.frequencia
        proxima_data: $input.proxima_data ?? $recorrencia.proxima_data
        dia_referencia: $input.dia_referencia ?? $recorrencia.dia_referencia
        mes_referencia: $input.mes_referencia ?? $recorrencia.mes_referencia
        ativa: $input.ativa ?? $recorrencia.ativa
      }
    } as $atualizada
  }

  response = $atualizada
  guid = "67d2ed42-f01b-4ca1-aea7-cd9284394e50"
}
