# Design

A rota `POST auth/avatar` receberá o arquivo no campo `avatar`, chamará
`storage.create_image` com `access = "public"` e salvará o objeto resultante em
`user.avatar_url`. A resposta existente já retorna esse campo para o cliente.
