query "transacoes/{transacao_id}" verb=PATCH {
  api_group = "cashsave"
  auth = "user"

  input {
    int transacao_id
    int? conta_id?
    int? categoria_id?
    enum tipo? {
      values = ["receita", "despesa"]
    }
  
    text? descricao? filters=trim
    int? valor_centavos? filters=min:1
    date? data?
    text? observacoes? filters=trim
  }

  stack {
    db.query transacoes {
      where = $db.transacoes.id == $input.transacao_id && $db.transacoes.usuario_id == $auth.id
      return = {type: "single"}
    } as $transacao
  
    precondition ($transacao != null) {
      error_type = "accessdenied"
      error = "Transação não encontrada."
    }
  
    var $conta_id {
      value = $input.conta_id ?? $transacao.conta_id
    }
  
    var $categoria_id {
      value = $input.categoria_id ?? $transacao.categoria_id
    }
  
    var $tipo {
      value = $input.tipo ?? $transacao.tipo
    }
  
    db.query contas {
      where = $db.contas.id == $conta_id && $db.contas.usuario_id == $auth.id
      return = {type: "single"}
    } as $conta
  
    precondition ($conta_id == null || $conta != null) {
      error_type = "accessdenied"
      error = "Conta não encontrada."
    }
  
    db.query categorias {
      where = $db.categorias.id == $categoria_id && ($db.categorias.usuario_id == $auth.id || $db.categorias.usuario_id == null) && $db.categorias.tipo == $tipo
      return = {type: "single"}
    } as $categoria
  
    precondition ($categoria_id == null || $categoria != null) {
      error_type = "accessdenied"
      error = "Categoria inválida."
    }
  
    db.edit transacoes {
      field_name = "id"
      field_value = $transacao.id
      data = {
        conta_id      : $input.conta_id ?? $transacao.conta_id
        categoria_id  : $input.categoria_id ?? $transacao.categoria_id
        tipo          : $tipo
        descricao     : $input.descricao ?? $transacao.descricao
        valor_centavos: $input.valor_centavos ?? $transacao.valor_centavos
        data          : $input.data ?? $transacao.data
        observacoes   : $input.observacoes ?? $transacao.observacoes
      }
    } as $atualizada
  }

  response = $atualizada
  guid = "UYMTwi-sDM2HYCP6gQ4Bc_MMjXo"
}