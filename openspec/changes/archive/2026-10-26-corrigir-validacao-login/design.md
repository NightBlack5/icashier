# Design

## Context

A rota de login já busca o usuário, verifica a senha com a função nativa do Xano e cria o token. O problema está na precondição que trata o resultado booleano da verificação.

## Goals / Non-Goals

**Goals:**

- Fazer a precondição falhar somente quando a senha não for válida.
- Manter a mensagem de erro genérica e o restante do contrato da API.

**Non-Goals:**

- Alterar o modelo de usuário, hashes existentes, expiração do token ou formulário do frontend.

## Decisions

- Inverter a condição da precondição de senha para negar o resultado válido. Isso corrige a causa raiz sem trocar o mecanismo seguro de verificação.
- Publicar apenas `auth/login_POST.xs`, evitando sincronização de outras rotas.

## Risks / Trade-offs

- [Risco] Uma publicação incorreta poderia afetar o login remoto. -> Mitigação: executar preview limitado ao arquivo, publicar com `--include` e validar a compilação e a rota local.
