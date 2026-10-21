# Design

O estado extrairá a primeira URL não vazia entre `url`, `public_url`,
`signed_url`, `download_url` e `link`, incluindo um objeto `file` aninhado.
Sem URL, o handler continuará recusando a atualização para evitar exibir
sucesso falso.
