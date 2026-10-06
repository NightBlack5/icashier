query categorias verb=POST {
  api_group = "cashsave"
  auth = "user"

  input {
    text nome filters=trim
    enum tipo {
      values = ["receita", "despesa"]
    }
    text? icone? filters=trim
    text? cor? filters=trim
  }

  stack {
    db.add categorias {
      data = {
        usuario_id: $auth.id
        nome: $input.nome
        tipo: $input.tipo
        icone: $input.icone
        cor: $input.cor
        criada_pelo_usuario: true
      }
    } as $categoria
  }

  response = $categoria
  guid = "yIQ0croNXInSItWV2RceYm2l87w"
}
