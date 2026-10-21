query "preferencias_usuario/me" verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
  }

  stack {
    db.query preferencias_usuario {
      where = $db.preferencias_usuario.usuario_id == $auth.id
      return = {type: "single"}
    } as $preferencias
  }

  response = $preferencias
  guid = "Fr6qMcVQkdB2NfXje-JIbxh4d48"
}