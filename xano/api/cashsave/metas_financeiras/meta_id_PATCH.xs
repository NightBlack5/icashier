query "metas_financeiras/{meta_id}" verb=PATCH {
  api_group = "cashsave"
  auth = "user"

  input {
    int meta_id
    text? nome? filters=trim
    text? descricao? filters=trim
    int? valor_objetivo_centavos? filters=min:1
    int? valor_atual_centavos? filters=min:0
    date? data_alvo?
    enum status? {
      values = ["ativa", "concluida", "arquivada"]
    }
  }

  stack {
    db.query metas_financeiras {
      where = $db.metas_financeiras.id == $input.meta_id && $db.metas_financeiras.usuario_id == $auth.id
      return = {type: "single"}
    } as $meta

    precondition ($meta != null) {
      error_type = "accessdenied"
      error = "Meta financeira não encontrada."
    }

    db.edit metas_financeiras {
      field_name = "id"
      field_value = $meta.id
      data = {
        nome: $input.nome ?? $meta.nome
        descricao: $input.descricao ?? $meta.descricao
        valor_objetivo_centavos: $input.valor_objetivo_centavos ?? $meta.valor_objetivo_centavos
        valor_atual_centavos: $input.valor_atual_centavos ?? $meta.valor_atual_centavos
        data_alvo: $input.data_alvo ?? $meta.data_alvo
        status: $input.status ?? $meta.status
      }
    } as $atualizada
  }

  response = $atualizada
  guid = "zF0Wg8xeH6sWJfMqzuYtYz-iRvo"
}
