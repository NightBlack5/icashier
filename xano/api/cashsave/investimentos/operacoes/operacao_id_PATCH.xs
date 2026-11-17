query "investimentos/operacoes/{operacao_id}" verb=PATCH {
  api_group = "cashsave"
  auth = "user"

  input {
    int operacao_id
    text? ativo_codigo? filters=trim
    enum? ativo_categoria? {
      values = ["acao", "fii", "etf"]
    }
    enum? tipo? {
      values = ["compra", "venda"]
    }
    date? data?
    decimal? quantidade? filters=min:0.0001
    int? preco_unitario_centavos? filters=min:1
    int? custos_centavos? filters=min:0
    text? observacoes? filters=trim
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

    var $ativo_codigo { value = ($input.ativo_codigo|to_upper) ?? $operacao.ativo_codigo }
    var $tipo { value = $input.tipo ?? $operacao.tipo }
    var $data { value = $input.data ?? $operacao.data }
    var $quantidade { value = $input.quantidade ?? $operacao.quantidade }

    conditional {
      if ($ativo_codigo != $operacao.ativo_codigo) {
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
        } as $historico_antigo_validado
      }
    }

    function.run "CashSave/validar_historico_operacoes" {
      input = {
        usuario_id: $auth.id
        ativo_codigo: $ativo_codigo
        operacao_id: $operacao.id
        tipo: $tipo
        data: $data
        quantidade: $quantidade
      }
    } as $historico_novo_validado

    db.edit investimento_operacoes {
      field_name = "id"
      field_value = $operacao.id
      data = {
        ativo_codigo: $ativo_codigo
        ativo_categoria: $input.ativo_categoria ?? $operacao.ativo_categoria
        tipo: $tipo
        data: $data
        quantidade: $quantidade
        preco_unitario_centavos: $input.preco_unitario_centavos ?? $operacao.preco_unitario_centavos
        custos_centavos: $input.custos_centavos ?? $operacao.custos_centavos
        observacoes: $input.observacoes ?? $operacao.observacoes
        atualizado_em: now
      }
    } as $atualizada
  }

  response = $atualizada
  guid = "ROm7gTjAlvRmNqN9VbNdq52b"
}
