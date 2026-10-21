# Design

A disponibilidade do controle será derivada da sessão autenticada, não da
presença opcional de `avatar_url` no registro retornado por `resumo`. O upload
continuará usando `POST /auth/avatar` com multipart e o token Bearer. O estado
será atualizado somente após o Xano retornar uma URL de avatar válida.
