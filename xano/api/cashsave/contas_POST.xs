query contas verb=POST {
  api_group = "cashsave"
  auth = "user"

  input {
    text nome filters=trim
    enum tipo {
      values = ["conta_corrente", "poupanca", "carteira", "cartao_credito", "outro"]
    }
    text? instituicao? filters=trim
    int? saldo_inicial_centavos?
  }

  stack {
    db.add contas {
      data = {
        usuario_id: $auth.id
        nome: $input.nome
        tipo: $input.tipo
        instituicao: $input.instituicao
        saldo_inicial_centavos: $input.saldo_inicial_centavos
        ativa: true
      }
    } as $conta
  }

  response = $conta
  guid = "Lo2APyTHzlaJoQQ69-9TxY8QmFM"
}
