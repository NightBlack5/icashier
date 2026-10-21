// Perfil do usuario com dados complementares
table perfis {
  auth = false

  schema {
    int id
    int usuario_id {
      table = "user"
    }
  
    text nome filters=trim
    timestamp criado_em?=now
    timestamp atualizado_em?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree|unique", field: [{name: "usuario_id"}]}
  ]

  guid = "M8aAWnulprX0eMloMGusqEcAKqM"
  items = []
}