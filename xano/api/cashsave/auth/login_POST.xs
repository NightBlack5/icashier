query "auth/login" verb=POST {
  api_group = "cashsave"

  input {
    email email filters=trim|lower
    text password
  }

  stack {
    db.get user {
      field_name = "email"
      field_value = $input.email
      output = ["id", "name", "email", "password", "avatar_url"]
    } as $user

    precondition ($user != null) {
      error_type = "accessdenied"
      error = "E-mail ou senha inválidos."
    }

    security.check_password {
      text_password = $input.password
      hash_password = $user.password
    } as $password_valid

    // The precondition continues only when the password is valid.
    // An invalid result stops the request before an auth token is created.
    precondition ($password_valid == true) {
      error_type = "accessdenied"
      error = "E-mail ou senha inválidos."
    }

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
      avatar_url: $user.avatar_url
    }
  }
  guid = "j3xfCsZxD0h2qjy264yqT7zutYg"
}
