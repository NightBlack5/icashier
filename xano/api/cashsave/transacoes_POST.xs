query transacoes verb=POST {
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
    date data
    text? observacoes? filters=trim
  }

  stack {
    db.query contas {
      where = $db.contas.id == $input.conta_id && $db.contas.usuario_id == $auth.id
      return = {type: "single"}
    } as $conta

    precondition ($input.conta_id == null || $conta != null) {
      error_type = "accessdenied"
      error = "Conta não encontrada."
    }

    db.query categorias {
      where = $db.categorias.id == $input.categoria_id && ($db.categorias.usuario_id == $auth.id || $db.categorias.usuario_id == null) && $db.categorias.tipo == $input.tipo
      return = {type: "single"}
    } as $categoria

    precondition ($input.categoria_id == null || $categoria != null) {
      error_type = "accessdenied"
      error = "Categoria inválida."
    }

    db.add transacoes {
      data = {
        usuario_id: $auth.id
        conta_id: $input.conta_id
        categoria_id: $input.categoria_id
        tipo: $input.tipo
        descricao: $input.descricao
        valor_centavos: $input.valor_centavos
        data: $input.data
        observacoes: $input.observacoes
      }
    } as $transacao
  }

  response = $transacao
  guid = "8gwOKPNUThIkXSYkfedITHgozsg"
}
