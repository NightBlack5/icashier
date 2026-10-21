query "contas_a_pagar/{conta_a_pagar_id}/pagar" verb=POST {
  api_group = "cashsave"
  auth = "user"

  input {
    int conta_a_pagar_id
    date? data_pagamento?
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
  
    db.edit contas_a_pagar {
      field_name = "id"
      field_value = $conta.id
      data = {status: "paga", data_pagamento: $input.data_pagamento}
    } as $atualizada
  }

  response = $atualizada
  guid = "3isr_1-LxEghfl7nRNkGdd6tcuU"
}