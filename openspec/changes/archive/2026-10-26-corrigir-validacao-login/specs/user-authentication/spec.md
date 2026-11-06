# Spec Delta

## Purpose

Define o comportamento confiável de entrada de usuários existentes no CashSave, aceitando senhas corretas e recusando credenciais inválidas sem revelar qual dado falhou.

## ADDED Requirements

### Requirement: aceitar credenciais válidas
O sistema SHALL autenticar um usuário quando o e-mail existir e a senha fornecida corresponder à senha armazenada.

#### Scenario: login bem-sucedido
- **WHEN** o usuário envia e-mail existente e senha correta
- **THEN** o sistema retorna um token de sessão e os dados básicos do usuário

### Requirement: rejeitar credenciais inválidas
O sistema SHALL rejeitar e-mail inexistente ou senha incorreta com uma mensagem genérica de credenciais inválidas.

#### Scenario: senha incorreta
- **WHEN** o usuário envia e-mail existente com senha incorreta
- **THEN** o sistema não cria sessão e informa que o e-mail ou a senha são inválidos
