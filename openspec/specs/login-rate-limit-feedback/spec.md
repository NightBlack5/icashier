# login-rate-limit-feedback Specification

## Purpose

Oferece uma resposta clara e segura quando o provedor de autenticação limita temporariamente novas tentativas de login.

## Requirements

### Requirement: informar bloqueio temporário

O sistema SHALL converter uma resposta HTTP 429 durante o login em uma mensagem em português que informe a necessidade de aguardar antes de tentar novamente.

#### Scenario: limite de tentativas atingido

- **WHEN** o endpoint de login responde HTTP 429
- **THEN** a tela informa que o limite temporário foi atingido e não exibe a mensagem técnica original do provedor

### Requirement: preservar erros de credenciais

O sistema SHALL continuar exibindo a mensagem de credenciais inválidas para respostas de autenticação que não sejam limitação temporária.

#### Scenario: senha inválida

- **WHEN** o endpoint responde com erro de credenciais sem status 429
- **THEN** a tela informa que o e-mail ou a senha são inválidos

