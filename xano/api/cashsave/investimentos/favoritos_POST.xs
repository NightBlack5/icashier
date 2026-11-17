query "investimentos/favoritos" verb=POST {
  api_group = "cashsave"
  auth = "user"

  input {
    text ativo_codigo filters=trim
    enum ativo_categoria {
      values = ["acao", "fii", "etf"]
    }
  }

  stack {
    precondition ($input.ativo_codigo != "") {
      error_type = "inputerror"
      error = "Informe o código do ativo."
    }

    db.query investimento_favoritos {
      where = $db.investimento_favoritos.usuario_id == $auth.id && $db.investimento_favoritos.ativo_codigo == ($input.ativo_codigo|to_upper)
      return = {type: "single"}
    } as $favorito_existente

    precondition ($favorito_existente == null) {
      error_type = "inputerror"
      error = "Este ativo já está nos favoritos."
    }

    db.add investimento_favoritos {
      data = {
        usuario_id: $auth.id
        ativo_codigo: $input.ativo_codigo|to_upper
        ativo_categoria: $input.ativo_categoria
      }
    } as $favorito
  }

  response = $favorito
  guid = "fAV0R1T0sP0sTC4shS4v3"
}
