# Design

O componente `rx.upload` chamará o mesmo evento `enviar_foto_perfil` no
`on_drop`, usando `rx.upload_files("profile-photo")`. O handler continuará
validando o arquivo e só atualizará o avatar após confirmação do Xano. O botão
existente permanece como reenvio manual.
