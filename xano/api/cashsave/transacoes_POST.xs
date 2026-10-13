query transacoes verb=POST {
  api_group = "cashsave"
  auth = "user"

  input {
    int? conta_id?
    int? categoria_id?
    int? recorrencia_id?
    date? recorrencia_data?
    enum tipo {
      values = ["receita", "despesa"]
    }
    text descricao filters=trim
    int valor_centavos filters=min:1
    date data
    text? observacoes? filters=trim
  }

  stack {
    db.query recorrencias {
      where = $db.recorrencias.id == $input.recorrencia_id && $db.recorrencias.usuario_id == $auth.id
      return = {type: "single"}
    } as $recorrencia

    precondition ($input.recorrencia_id == null || $recorrencia != null) {
      error_type = "accessdenied"
      error = "Recorrência não encontrada."
    }

    precondition (
      ($input.recorrencia_id == null && $input.recorrencia_data == null)
      || ($input.recorrencia_id != null && $input.recorrencia_data != null)
    ) {
      error_type = "inputerror"
      error = "Informe a data e a recorrência juntas."
    }

    db.query transacoes {
      where = $db.transacoes.usuario_id == $auth.id
        && $db.transacoes.recorrencia_id == $input.recorrencia_id
        && $db.transacoes.recorrencia_data == $input.recorrencia_data
      return = {type: "single"}
    } as $ocorrencia_existente

    precondition (
      $input.recorrencia_id == null || $ocorrencia_existente == null
    ) {
      error_type = "inputerror"
      error = "Esta ocorrência recorrente já foi registrada."
    }

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
        recorrencia_id: $input.recorrencia_id
        tipo: $input.tipo
        descricao: $input.descricao
        valor_centavos: $input.valor_centavos
        data: $input.data
        recorrencia_data: $input.recorrencia_data
        observacoes: $input.observacoes
      }
    } as $transacao
  }

  response = $transacao
  guid = "8gwOKPNUThIkXSYkfedITHgozsg"
}
