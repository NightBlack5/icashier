function "CashSave/validar_historico_operacoes" {
  input {
    int usuario_id
    text ativo_codigo
    int? operacao_id?
    enum? tipo? {
      values = ["compra", "venda"]
    }
    date? data?
    decimal? quantidade?
    bool? excluir?=false
  }

  stack {
    db.query investimento_operacoes {
      where = $db.investimento_operacoes.usuario_id == $input.usuario_id && $db.investimento_operacoes.ativo_codigo == $input.ativo_codigo
      sort = {
        investimento_operacoes.data: "asc"
        investimento_operacoes.id: "asc"
      }
    } as $operacoes

    var $quantidade_disponivel {
      value = 0
    }

    var $candidato_aplicado {
      value = false
    }

    foreach ($operacoes) {
      each as $item {
        conditional {
          if ($input.excluir != true && $candidato_aplicado == false && ($input.data < $item.data || ($input.data == $item.data && $input.operacao_id != null && $input.operacao_id < $item.id))) {
            function.run "CashSave/aplicar_operacao_investimento" {
              input = {
                quantidade_disponivel: $quantidade_disponivel
                tipo: $input.tipo
                quantidade: $input.quantidade
              }
            } as $quantidade_disponivel

            var $candidato_aplicado {
              value = true
            }
          }
        }

        conditional {
          if ($input.excluir != true && $candidato_aplicado == false && $input.operacao_id != null && $input.operacao_id == $item.id) {
            function.run "CashSave/aplicar_operacao_investimento" {
              input = {
                quantidade_disponivel: $quantidade_disponivel
                tipo: $input.tipo
                quantidade: $input.quantidade
              }
            } as $quantidade_disponivel

            var $candidato_aplicado {
              value = true
            }
          }
        }

        conditional {
          if ($input.operacao_id == null || $item.id != $input.operacao_id) {
            function.run "CashSave/aplicar_operacao_investimento" {
              input = {
                quantidade_disponivel: $quantidade_disponivel
                tipo: $item.tipo
                quantidade: $item.quantidade
              }
            } as $quantidade_disponivel
          }
        }
      }
    }

    conditional {
      if ($input.excluir != true && $candidato_aplicado == false) {
        function.run "CashSave/aplicar_operacao_investimento" {
          input = {
            quantidade_disponivel: $quantidade_disponivel
            tipo: $input.tipo
            quantidade: $input.quantidade
          }
        } as $quantidade_disponivel
      }
    }
  }

  response = {valid: true}
  guid = "m4P1bt1hq8ZzL3eUErh3fv0m"
}
