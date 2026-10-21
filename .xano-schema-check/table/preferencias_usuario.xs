// Preferências regionais e notificações da conta CashSave
table preferencias_usuario {
  auth = false

  schema {
    int id
    int usuario_id {
      table = "user"
    }
  
    text moeda?=BRL
    text localidade?="pt-BR"
    text fuso_horario?="America/Sao_Paulo"
    bool notificacoes_vencimento?=true
    bool notificacoes_orcamento?=true
    timestamp criado_em?=now
    timestamp atualizado_em?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "usuario_id"}]}
  ]

  guid = "ZYEmtxph20PqtReexeGuELBKLDU"
  items = [
    {
      id                     : 1
      usuario_id             : 2
      moeda                  : "BRL"
      localidade             : "pt-BR"
      fuso_horario           : "America/Sao_Paulo"
      notificacoes_vencimento: true
      notificacoes_orcamento : true
      criado_em              : 1791322326363
      atualizado_em          : 0
    }
    {
      id                     : 2
      usuario_id             : 3
      moeda                  : "BRL"
      localidade             : "pt-BR"
      fuso_horario           : "America/Sao_Paulo"
      notificacoes_vencimento: true
      notificacoes_orcamento : true
      criado_em              : 1791323545841
      atualizado_em          : 0
    }
    {
      id                     : 3
      usuario_id             : 4
      moeda                  : "BRL"
      localidade             : "pt-BR"
      fuso_horario           : "America/Sao_Paulo"
      notificacoes_vencimento: true
      notificacoes_orcamento : true
      criado_em              : 1792447823612
      atualizado_em          : 0
    }
    {
      id                     : 4
      usuario_id             : 5
      moeda                  : "BRL"
      localidade             : "pt-BR"
      fuso_horario           : "America/Sao_Paulo"
      notificacoes_vencimento: true
      notificacoes_orcamento : true
      criado_em              : 1792450024797
      atualizado_em          : 0
    }
    {
      id                     : 5
      usuario_id             : 6
      moeda                  : "BRL"
      localidade             : "pt-BR"
      fuso_horario           : "America/Sao_Paulo"
      notificacoes_vencimento: true
      notificacoes_orcamento : true
      criado_em              : 1792451597827
      atualizado_em          : 0
    }
  ]
}