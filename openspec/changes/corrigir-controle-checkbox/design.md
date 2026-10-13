# Design: corrigir-controle-checkbox

## Abordagem

Centralizar a normalização dos valores de checkbox no estado da aplicação, convertendo entradas de texto e booleano para um único formato de controle interno. Isso mantém a lógica do formulário compatível com o que o componente Reflex entrega em eventos de `on_change`.

## Fluxo de autenticação

- Login: o checkbox de "Lembrar de mim" deve alternar entre "true" e "false" e persistir o e-mail salvo apenas quando a opção estiver marcada.
- Cadastro: o checkbox de termos deve traduzir qualquer entrada do componente para um booleano válido antes de validar a criação da conta.

## Verificação

A correção é focada em API pública da UI e estado local; não há mudança de contrato externo com o Xano nem alteração de endpoints.
