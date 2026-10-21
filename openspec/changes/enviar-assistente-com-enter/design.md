# Design

O campo de mensagem e o botão serão filhos de `rx.form`, cujo `on_submit`
chamará `AppState.enviar_mensagem_assistente`. O botão receberá
`type="submit"`, permitindo que o navegador dispare o mesmo evento ao
pressionar Enter no input. O comportamento visual e o botão permanecerão
inalterados.
