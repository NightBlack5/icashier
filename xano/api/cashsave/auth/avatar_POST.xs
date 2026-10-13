query "auth/avatar" verb=POST {
  api_group = "cashsave"
  auth = "user"

  input {
    file avatar
  }

  stack {
    db.patch user {
      field_name = "id"
      field_value = $auth.id
      data = {
        avatar_url: $input.avatar
      }
    } as $user
  }

  response = {
    user: {
      id: $user.id
      name: $user.name
      email: $user.email
      avatar_url: $user.avatar_url
    }
  }
  guid = "b6fa1fa1-9e62-47d2-b4dd-8ab985ab4a93"
}
