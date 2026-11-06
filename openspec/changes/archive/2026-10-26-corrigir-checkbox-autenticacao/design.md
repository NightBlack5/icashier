# Design

Os controles serão renderizados com `rx.checkbox`, recebendo `checked` e
`on_change` diretamente. O estado `lembrar_email` continuará armazenado como
string no `LocalStorage`, e o handler existente continuará normalizando o
valor booleano emitido pelo componente.
