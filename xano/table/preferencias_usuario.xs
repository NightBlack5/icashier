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
    bool notificacoes_metas?=true
    timestamp criado_em?=now
    timestamp atualizado_em?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "usuario_id"}]}
  ]

  guid = "ZYEmtxph20PqtReexeGuELBKLDU"
}
