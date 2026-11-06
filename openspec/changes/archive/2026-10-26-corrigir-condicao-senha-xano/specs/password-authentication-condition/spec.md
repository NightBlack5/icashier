# Spec Delta

## Purpose

Garante que o login bloqueie somente senhas que não correspondem ao hash armazenado e permita a criação de sessão para senhas corretas.

## ADDED Requirements

### Requirement: bloquear somente senha inválida
O sistema SHALL interromper o login somente quando a verificação de senha retornar falso.

#### Scenario: senha correta
- **WHEN** a verificação retorna verdadeiro
- **THEN** o login continua para a criação do token

#### Scenario: senha incorreta
- **WHEN** a verificação retorna falso
- **THEN** o login é interrompido e nenhum token é criado
