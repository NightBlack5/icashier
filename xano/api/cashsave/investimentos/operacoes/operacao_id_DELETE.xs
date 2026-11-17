query "investimentos/operacoes/{operacao_id}" verb=DELETE {
  api_group = "cashsave"
  auth = "user"

  input {
    int operacao_id
  }

  stack {
    db.query investimento_operacoes {
      where = $db.investimento_operacoes.id == $input.operacao_id && $db.investimento_operacoes.usuario_id == $auth.id
      return = {type: "single"}
    } as $operacao

    precondition ($operacao != null) {
      error_type = "accessdenied"
      error = "Operação não encontrada."
    }

    function.run "CashSave/validar_historico_operacoes" {
      input = {
        usuario_id: $auth.id
        ativo_codigo: $operacao.ativo_codigo
        operacao_id: $operacao.id
        tipo: $operacao.tipo
        data: $operacao.data
        quantidade: $operacao.quantidade
        excluir: true
      }
    } as $historico_validado

    db.del investimento_operacoes {
      field_name = "id"
      field_value = $operacao.id
    }
  }

  response = {success: true}
  guid = "ZJxagjVhP7cmmXyUEtuYR-CC"
}
