query "assistente/conversas" verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
  }

  stack {
    db.query agent_conversation {
      where = $db.agent_conversation.owner_user == $auth.id
      sort = {agent_conversation.last_message_at: "desc"}
      return = {type: "list"}
      output = ["id", "title", "last_message_at"]
    } as $conversas
  }

  response = $conversas
  guid = "ikiq9GYYerzcTnc1S_h06rkfDAU"
}