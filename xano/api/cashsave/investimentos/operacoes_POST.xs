query "investimentos/operacoes" verb=POST {
  api_group = "cashsave"
  auth = "user"

  input {
    text ativo_codigo filters=trim
    enum ativo_categoria {
      values = ["acao", "fii", "etf"]
    }
    enum tipo {
      values = ["compra", "venda"]
    }
    date data
    decimal quantidade filters=min:0.0001
    int preco_unitario_centavos filters=min:1
    int? custos_centavos?=0 filters=min:0
    text? observacoes? filters=trim
  }

  stack {
    precondition ($input.ativo_codigo != "") {
      error_type = "inputerror"
      error = "Informe o código do ativo."
    }

    function.run "CashSave/validar_historico_operacoes" {
      input = {
        usuario_id: $auth.id
        ativo_codigo: $input.ativo_codigo|to_upper
        tipo: $input.tipo
        data: $input.data
        quantidade: $input.quantidade
      }
    } as $historico_validado

    db.add investimento_operacoes {
      data = {
        usuario_id: $auth.id
        ativo_codigo: $input.ativo_codigo|to_upper
        ativo_categoria: $input.ativo_categoria
        tipo: $input.tipo
        data: $input.data
        quantidade: $input.quantidade
        preco_unitario_centavos: $input.preco_unitario_centavos
        custos_centavos: $input.custos_centavos ?? 0
        observacoes: $input.observacoes
      }
    } as $operacao
  }

  response = $operacao
  guid = "MSiYiKvEfE4R-vq3jMqX4TMA"
}
