query "contas/{conta_id}" verb=PATCH {
  api_group = "cashsave"
  auth = "user"

  input {
    int conta_id
    text? nome? filters=trim
    enum tipo? {
      values = [
        "conta_corrente"
        "poupanca"
        "carteira"
        "cartao_credito"
        "outro"
      ]
    }
  
    text? instituicao? filters=trim
    int? saldo_inicial_centavos?
    bool? ativa?
  }

  stack {
    db.query contas {
      where = $db.contas.id == $input.conta_id && $db.contas.usuario_id == $auth.id
      return = {type: "single"}
    } as $conta
  
    precondition ($conta != null) {
      error_type = "accessdenied"
      error = "Conta não encontrada."
    }
  
    db.edit contas {
      field_name = "id"
      field_value = $conta.id
      data = {
        nome                  : $input.nome ?? $conta.nome
        tipo                  : $input.tipo ?? $conta.tipo
        instituicao           : $input.instituicao ?? $conta.instituicao
        saldo_inicial_centavos: $input.saldo_inicial_centavos ?? $conta.saldo_inicial_centavos
        ativa                 : $input.ativa ?? $conta.ativa
      }
    } as $atualizada
  }

  response = $atualizada
  guid = "KdX0R9yM3mQX-PhO_JEsGc05fe4"
}