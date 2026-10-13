# Proposta: corrigir-controle-checkbox

## Por que

A tela de autenticação do CashSave expõe controles de checkbox para aceitar termos e lembrar e-mail. O comportamento atual não está consistente com o tipo de valor enviado pelos eventos do Reflex e isso pode impedir a interação correta do formulário.

## O que muda

- Normalizar os valores emitidos pelos checkboxes antes de atualizar o estado.
- Garantir que a UI preserve a marcação correta e o comportamento do formulário.
- Manter a validação de login/cadastro funcionando sem regressões para usuários existentes.

## Escopo

- Alterações em `CashSave/pages/auth.py` e `CashSave/state.py`.
- Sem mudança na API do Xano ou no fluxo principal de autenticação.

## Impacto

- Fluxo de login/cadastro em páginas de acesso.
- Estado local de `lembrar_email` e `aceitou_termos`.
- Validação dos campos e exibição de mensagens de erro.
