query orcamentos verb=POST {
  api_group = "cashsave"
  auth = "user"

  input {
    text nome filters=trim
    int? categoria_id?
    int limite_centavos filters=min:1
    enum periodicidade {
      values = ["semanal", "mensal", "trimestral", "anual", "personalizada"]
    }
    date data_inicio
    date data_fim
  }

  stack {
    db.query categorias {
      where = $db.categorias.id == $input.categoria_id && ($db.categorias.usuario_id == $auth.id || $db.categorias.usuario_id == null) && $db.categorias.tipo == "despesa"
      return = {type: "single"}
    } as $categoria

    precondition ($input.categoria_id == null || $categoria != null) {
      error_type = "accessdenied"
      error = "Categoria inválida."
    }

    precondition ($input.data_fim >= $input.data_inicio) {
      error_type = "inputerror"
      error = "A data final deve ser igual ou posterior à data inicial."
    }

    db.add orcamentos {
      data = {
        usuario_id: $auth.id
        nome: $input.nome
        categoria_id: $input.categoria_id
        limite_centavos: $input.limite_centavos
        periodicidade: $input.periodicidade
        data_inicio: $input.data_inicio
        data_fim: $input.data_fim
        ativo: true
      }
    } as $orcamento
  }

  response = $orcamento
  guid = "6yOqwyr77qXQMEpB8shK4564j_A"
}
