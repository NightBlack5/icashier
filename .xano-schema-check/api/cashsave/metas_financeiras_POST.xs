query metas_financeiras verb=POST {
  api_group = "cashsave"
  auth = "user"

  input {
    text nome filters=trim
    text? descricao? filters=trim
    int valor_objetivo_centavos filters=min:1
    int? valor_atual_centavos? filters=min:0
    date? data_alvo?
  }

  stack {
    db.add metas_financeiras {
      data = {
        usuario_id             : $auth.id
        nome                   : $input.nome
        descricao              : $input.descricao
        valor_objetivo_centavos: $input.valor_objetivo_centavos
        valor_atual_centavos   : $input.valor_atual_centavos
        data_alvo              : $input.data_alvo
        status                 : "ativa"
      }
    } as $meta
  }

  response = $meta
  guid = "4teBhvuHc4kHlighgkTxE97_sHQ"
}