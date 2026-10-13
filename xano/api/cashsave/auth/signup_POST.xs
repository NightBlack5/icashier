query "auth/signup" verb=POST {
  api_group = "cashsave"

  input {
    text name filters=trim
    email email filters=trim|lower
    text phone filters=trim
    password password filters=min:8|minAlpha:1|minDigit:1
  }

  stack {
    precondition ($input.name != "") {
      error_type = "inputerror"
      error = "Informe seu nome."
    }

    db.get user {
      field_name = "email"
      field_value = $input.email
    } as $existing_user

    precondition ($existing_user == null) {
      error_type = "accessdenied"
      error = "Este e-mail já está cadastrado."
    }

    db.add user {
      data = {
        name: $input.name
        email: $input.email
        phone: $input.phone
        password: $input.password
        role: "member"
      }
    } as $user

    db.add preferencias_usuario {
      data = {
        usuario_id: $user.id
      }
    } as $preferences

    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 86400
      id = $user.id
    } as $authToken
  }

  response = {
    authToken: $authToken
    user: {
      id: $user.id
      name: $user.name
      email: $user.email
    }
  }
  guid = "pfX3DpVYRsDfE7sCAlaCqog_Osk"
}
