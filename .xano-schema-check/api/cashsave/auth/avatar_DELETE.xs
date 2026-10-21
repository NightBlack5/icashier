query "auth/avatar" verb=DELETE {
  api_group = "cashsave"
  auth = "user"

  input {
  }

  stack {
    db.patch user {
      field_name = "id"
      field_value = $auth.id
      data = {avatar_url: null}
    } as $user
  }

  response = {
    user: ```
      {
        id: $user.id
        name: $user.name
        email: $user.email
        avatar_url: $user.avatar_url
      }
      ```
  }

  guid = "ba1add38-cc10-4669-aeea-c783c715d024"
}