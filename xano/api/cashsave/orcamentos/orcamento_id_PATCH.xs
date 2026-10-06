query "orcamentos/{orcamento_id}" verb=PATCH {
  api_group = "cashsave"
  auth = "user"

  input {
    int orcamento_id
    text? nome? filters=trim
    int? categoria_id?
    int? limite_centavos? filters=min:1
    enum periodicidade? {
      values = ["semanal", "mensal", "trimestral", "anual", "personalizada"]
    }
    date? data_inicio?
    date? data_fim?
    bool? ativo?
  }

  stack {
    db.query orcamentos {
      where = $db.orcamentos.id == $input.orcamento_id && $db.orcamentos.usuario_id == $auth.id
      return = {type: "single"}
    } as $orcamento

    precondition ($orcamento != null) {
      error_type = "accessdenied"
      error = "Orçamento não encontrado."
    }

    var $categoria_id { value = $input.categoria_id ?? $orcamento.categoria_id }
    var $data_inicio { value = $input.data_inicio ?? $orcamento.data_inicio }
    var $data_fim { value = $input.data_fim ?? $orcamento.data_fim }

    db.query categorias {
      where = $db.categorias.id == $categoria_id && ($db.categorias.usuario_id == $auth.id || $db.categorias.usuario_id == null) && $db.categorias.tipo == "despesa"
      return = {type: "single"}
    } as $categoria

    precondition ($categoria_id == null || $categoria != null) {
      error_type = "accessdenied"
      error = "Categoria inválida."
    }

    precondition ($data_fim >= $data_inicio) {
      error_type = "inputerror"
      error = "A data final deve ser igual ou posterior à data inicial."
    }

    db.edit orcamentos {
      field_name = "id"
      field_value = $orcamento.id
      data = {
        nome: $input.nome ?? $orcamento.nome
        categoria_id: $categoria_id
        limite_centavos: $input.limite_centavos ?? $orcamento.limite_centavos
        periodicidade: $input.periodicidade ?? $orcamento.periodicidade
        data_inicio: $data_inicio
        data_fim: $data_fim
        ativo: $input.ativo ?? $orcamento.ativo
      }
    } as $atualizado
  }

  response = $atualizado
  guid = "RWlFU56EiNBW-c5d3KLVqdxIqEY"
}
