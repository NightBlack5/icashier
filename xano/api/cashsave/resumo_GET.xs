// Retorna resumo financeiro do usuario por periodo com colecoes completas
// Retorna usuario, transacoes, contas, categorias, contas a pagar, orcamentos, metas, recorrencias e preferencias
query resumo verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
    // Data inicial do periodo (opcional)
    date? data_inicio?

    // Data final do periodo (opcional)
    date? data_fim?

    // Filtrar por conta especifica (opcional)
    int? conta_id? {
      table = "contas"
    }
  }

  stack {
    // Consulta dados do usuario autenticado
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "name", "email", "created_at", "avatar_url"]
    } as $usuario

    // Consulta transacoes do usuario no periodo
    db.query transacoes {
      where = $db.transacoes.usuario_id == $auth.id && $db.transacoes.data >=? $input.data_inicio && $db.transacoes.data <=? $input.data_fim && $db.transacoes.conta_id ==? $input.conta_id
      return = {type: "list"}
    } as $transacoes

    // Consulta contas financeiras do usuario
    db.query contas {
      where = $db.contas.usuario_id == $auth.id
      return = {type: "list"}
    } as $contas

    // Consulta categorias globais e personalizadas do usuario
    db.query categorias {
      where = $db.categorias.usuario_id == $auth.id || $db.categorias.usuario_id == null
      return = {type: "list"}
    } as $categorias

    // Consulta contas a pagar do usuario
    db.query contas_a_pagar {
      where = $db.contas_a_pagar.usuario_id == $auth.id
      return = {type: "list"}
    } as $contas_a_pagar

    // Consulta orcamentos do usuario
    db.query orcamentos {
      where = $db.orcamentos.usuario_id == $auth.id
      return = {type: "list"}
    } as $orcamentos

    // Consulta metas financeiras do usuario
    db.query metas_financeiras {
      where = $db.metas_financeiras.usuario_id == $auth.id
      return = {type: "list"}
    } as $metas

    // Consulta recorrencias cadastradas pelo usuario
    db.query recorrencias {
      where = $db.recorrencias.usuario_id == $auth.id
      sort = {proxima_data: "asc"}
      return = {type: "list"}
    } as $recorrencias

    // Consulta preferencias do usuario
    db.query preferencias_usuario {
      where = $db.preferencias_usuario.usuario_id == $auth.id
      return = {type: "single"}
    } as $preferencias

    // Inicializa acumuladores de receitas e despesas
    var $total_receitas_centavos {
      value = 0
    }

    var $total_despesas_centavos {
      value = 0
    }

    var $qtd_receitas {
      value = 0
    }

    var $qtd_despesas {
      value = 0
    }

    // Itera para calcular totalizadores do periodo
    foreach ($transacoes) {
      each as $item {
        conditional {
          if ($item.tipo == "receita") {
            math.add $total_receitas_centavos {
              value = $item.valor_centavos
            }

            math.add $qtd_receitas {
              value = 1
            }
          }

          else {
            math.add $total_despesas_centavos {
              value = $item.valor_centavos
            }

            math.add $qtd_despesas {
              value = 1
            }
          }
        }
      }
    }

    // Calcula saldo liquido do periodo
    var $saldo_periodo_centavos {
      value = $total_receitas_centavos - $total_despesas_centavos
    }

    // Calcula total de transacoes processadas
    var $total_transacoes {
      value = $qtd_receitas + $qtd_despesas
    }
  }

  response = {
    usuario                : $usuario
    transacoes             : $transacoes
    contas                 : $contas
    categorias             : $categorias
    contas_a_pagar         : $contas_a_pagar
    orcamentos             : $orcamentos
    metas                  : $metas
    recorrencias           : $recorrencias
    preferencias           : $preferencias
    data_fim               : $input.data_fim
    data_inicio            : $input.data_inicio
    quantidade_despesas    : $qtd_despesas
    quantidade_receitas    : $qtd_receitas
    saldo_periodo_centavos : $saldo_periodo_centavos
    total_despesas_centavos: $total_despesas_centavos
    total_receitas_centavos: $total_receitas_centavos
    total_transacoes       : $total_transacoes
  }

  guid = "5ZzQxF7mlTD7QDjxbBGHv9Hr_-Q"
}
