query "preferencias_usuario/me" verb=PATCH {
  api_group = "cashsave"
  auth = "user"

  input {
    text? moeda?
    text? localidade?
    text? fuso_horario?
    bool? notificacoes_vencimento?
    bool? notificacoes_orcamento?
  }

  stack {
    db.query preferencias_usuario {
      where = $db.preferencias_usuario.usuario_id == $auth.id
      return = {type: "single"}
    } as $atuais
  
    db.add_or_edit preferencias_usuario {
      field_name = "usuario_id"
      field_value = $auth.id
      data = {
        usuario_id             : $auth.id
        moeda                  : $input.moeda ?? $atuais.moeda ?? "BRL"
        localidade             : $input.localidade ?? $atuais.localidade ?? "pt-BR"
        fuso_horario           : $input.fuso_horario ?? $atuais.fuso_horario ?? "America/Sao_Paulo"
        notificacoes_vencimento: $input.notificacoes_vencimento ?? $atuais.notificacoes_vencimento ?? true
        notificacoes_orcamento : $input.notificacoes_orcamento ?? $atuais.notificacoes_orcamento ?? true
      }
    } as $preferencias
  }

  response = $preferencias
  guid = "QmurDnS39wTQVmAf9YiOT2pZSD0"
}