query "investimentos/proventos" verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
  }

  stack {
    db.query investimento_proventos {
      where = $db.investimento_proventos.usuario_id == $auth.id
      sort = {investimento_proventos.data_pagamento: "desc"}
    } as $proventos
  }

  response = $proventos
  guid = "WUyYat3pggmEK3XqjwoZsZtR"
}
