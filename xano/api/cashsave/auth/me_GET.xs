query "auth/me" verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
  }

  stack {
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "name", "email"]
    } as $user
  }

  response = $user
  guid = "u_mvUVNnHzqVUc5nq0Hlb3LDWeU"
}
