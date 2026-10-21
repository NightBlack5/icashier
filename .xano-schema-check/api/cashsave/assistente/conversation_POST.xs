query "assistente/conversation" verb=POST {
  api_group = "cashsave"
  auth = "user"

  input {
    int? conversation_id?
    text message filters=trim|min:1
  }

  stack {
    db.query agent_conversation {
      where = $db.agent_conversation.id == $input.conversation_id && $db.agent_conversation.owner_user == $auth.id
      return = {type: "single"}
    } as $conversa
  
    precondition ($input.conversation_id == null || $input.conversation_id == 0 || $conversa != null) {
      error_type = "accessdenied"
      error = "Conversa não encontrada."
    }
  
    var $conversation_id {
      value = $input.conversation_id
    }
  
    conditional {
      if ($input.conversation_id == null || $input.conversation_id == 0) {
        db.add agent_conversation {
          enforce_hidden_fields = false
          data = {
            owner_user     : $auth.id
            title          : $input.message
            last_message_at: "now"
          }
        } as $nova_conversa
      
        var.update $conversation_id {
          value = $nova_conversa.id
        }
      }
    }
  
    db.query agent_message {
      where = $db.agent_message.conversation == $conversation_id
      sort = {agent_message.created_at: "asc"}
      return = {type: "list"}
      output = ["role", "content"]
    } as $historico
  
    var $mensagem_usuario {
      value = {}
        |set:"role":"user"
        |set:"content":$input.message
    }
  
    var $mensagens {
      value = $historico|push:$mensagem_usuario
    }
  
    ai.agent.run "Xano Example Agent" {
      args = {}|set:"messages":$mensagens
      allow_tool_execution = true
    } as $resposta_ia
  
    db.add agent_message {
      enforce_hidden_fields = false
      data = {
        created_at  : "now"
        conversation: $conversation_id
        role        : "user"
        content     : $input.message
      }
    } as $mensagem_salva
  
    db.add agent_message {
      enforce_hidden_fields = false
      data = {
        created_at  : "now"
        conversation: $conversation_id
        role        : "assistant"
        content     : $resposta_ia.result
      }
    } as $resposta_salva
  
    db.edit agent_conversation {
      field_name = "id"
      field_value = $conversation_id
      data = {
        title          : $conversa.title ?? $input.message
        last_message_at: "now"
      }
    } as $conversa_atualizada
  }

  response = {
    conversation_id: $conversation_id
    result         : $resposta_ia.result
  }

  guid = "rYjEf63Tp7x53ZmLJMX0t35nNxg"
}