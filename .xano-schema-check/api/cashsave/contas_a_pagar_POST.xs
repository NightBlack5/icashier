query contas_a_pagar verb=POST {
  api_group = "cashsave"
  auth = "user"

  input {
    int? conta_id?
    int? categoria_id?
    text descricao filters=trim
    int valor_centavos filters=min:1
    date data_vencimento
    enum recorrencia? {
      values = ["nenhuma", "semanal", "mensal", "anual"]
    }
  
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
      where = $db.categorias.id == $input.categoria_id && ($db.categorias.usuario_id == $auth.id || $db.categorias.usuario_id == null) && $db.categorias.tipo == "despesa"
      return = {type: "single"}
    } as $categoria
  
    precondition ($input.categoria_id == null || $categoria != null) {
      error_type = "accessdenied"
      error = "Categoria inválida."
    }
  
    db.add contas_a_pagar {
      data = {
        usuario_id     : $auth.id
        conta_id       : $input.conta_id
        categoria_id   : $input.categoria_id
        descricao      : $input.descricao
        valor_centavos : $input.valor_centavos
        data_vencimento: $input.data_vencimento
        status         : "pendente"
        recorrencia    : $input.recorrencia
        observacoes    : $input.observacoes
      }
    } as $conta
  }

  response = $conta
  guid = "2Ig00XFhL-8PkyApCichtj1Di-k"
}