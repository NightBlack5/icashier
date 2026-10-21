query "contas_a_pagar/{conta_a_pagar_id}" verb=PATCH {
  api_group = "cashsave"
  auth = "user"

  input {
    int conta_a_pagar_id
    int? conta_id?
    int? categoria_id?
    text? descricao? filters=trim
    int? valor_centavos? filters=min:1
    date? data_vencimento?
    enum status? {
      values = ["pendente", "paga", "cancelada"]
    }
  
    date? data_pagamento?
    enum recorrencia? {
      values = ["nenhuma", "semanal", "mensal", "anual"]
    }
  
    text? observacoes? filters=trim
  }

  stack {
    db.query contas_a_pagar {
      where = $db.contas_a_pagar.id == $input.conta_a_pagar_id && $db.contas_a_pagar.usuario_id == $auth.id
      return = {type: "single"}
    } as $conta
  
    precondition ($conta != null) {
      error_type = "accessdenied"
      error = "Conta a pagar não encontrada."
    }
  
    var $conta_id {
      value = $input.conta_id ?? $conta.conta_id
    }
  
    var $categoria_id {
      value = $input.categoria_id ?? $conta.categoria_id
    }
  
    db.query contas {
      where = $db.contas.id == $conta_id && $db.contas.usuario_id == $auth.id
      return = {type: "single"}
    } as $conta_financeira
  
    precondition ($conta_id == null || $conta_financeira != null) {
      error_type = "accessdenied"
      error = "Conta não encontrada."
    }
  
    db.query categorias {
      where = $db.categorias.id == $categoria_id && ($db.categorias.usuario_id == $auth.id || $db.categorias.usuario_id == null) && $db.categorias.tipo == "despesa"
      return = {type: "single"}
    } as $categoria
  
    precondition ($categoria_id == null || $categoria != null) {
      error_type = "accessdenied"
      error = "Categoria inválida."
    }
  
    db.edit contas_a_pagar {
      field_name = "id"
      field_value = $conta.id
      data = {
        conta_id       : $conta_id
        categoria_id   : $categoria_id
        descricao      : $input.descricao ?? $conta.descricao
        valor_centavos : $input.valor_centavos ?? $conta.valor_centavos
        data_vencimento: $input.data_vencimento ?? $conta.data_vencimento
        status         : $input.status ?? $conta.status
        data_pagamento : $input.data_pagamento ?? $conta.data_pagamento
        recorrencia    : $input.recorrencia ?? $conta.recorrencia
        observacoes    : $input.observacoes ?? $conta.observacoes
      }
    } as $atualizada
  }

  response = $atualizada
  guid = "_0RtUkYtwQ8r8VNZfvzGfFbhacs"
}