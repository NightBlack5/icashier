query "auth/avatar" verb=POST {
  api_group = "cashsave"
  auth = "user"

  input {
    file? avatar
  }

  stack {
    storage.create_image {
      value = $input.avatar
      access = "public"
      filename = ""
    } as $avatar_file
  
    db.patch user {
      field_name = "id"
      field_value = $auth.id
      data = {avatar_url: $avatar_file}
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

  guid = "b6fa1fa1-9e62-47d2-b4dd-8ab985ab4a93"
}