function "CashSave/aplicar_operacao_investimento" {
  input {
    decimal quantidade_disponivel
    enum tipo {
      values = ["compra", "venda"]
    }
    decimal quantidade
  }

  stack {
    var $quantidade_resultante {
      value = $input.quantidade_disponivel
    }

    conditional {
      if ($input.tipo == "compra") {
        var $quantidade_resultante {
          value = $input.quantidade_disponivel + $input.quantidade
        }
      }

      else {
        precondition ($input.quantidade <= $input.quantidade_disponivel) {
          error_type = "inputerror"
          error = "A venda excede a quantidade disponível na data da operação."
        }

        var $quantidade_resultante {
          value = $input.quantidade_disponivel - $input.quantidade
        }
      }
    }
  }

  response = $quantidade_resultante
  guid = "nkWXf4Z3x-T2-SFCKmjsBzUL"
}
