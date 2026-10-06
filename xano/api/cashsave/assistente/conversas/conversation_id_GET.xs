query "assistente/conversas/{conversation_id}" verb=GET {
  api_group = "cashsave"
  auth = "user"

  input {
    int conversation_id
  }

  stack {
    db.query agent_conversation {
      where = $db.agent_conversation.id == $input.conversation_id && $db.agent_conversation.owner_user == $auth.id
      return = {type: "single"}
      output = ["id", "title", "last_message_at"]
    } as $conversa

    precondition ($conversa != null) {
      error_type = "accessdenied"
      error = "Conversa não encontrada."
    }

    db.query agent_message {
      where = $db.agent_message.conversation == $conversa.id
      sort = {agent_message.created_at: "asc"}
      return = {type: "list"}
      output = ["id", "role", "content", "created_at"]
    } as $mensagens
  }

  response = {
    conversation: $conversa
    messages: $mensagens
  }
  guid = "8TM_nBhKnRdcIxTYS-2S5izFXSY"
}
