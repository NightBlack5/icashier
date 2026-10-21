# Spec Delta

## Purpose

Impede que o CashSave emita tokens para senhas incorretas sem bloquear usuários que fornecem a senha correspondente ao e-mail.

## ADDED Requirements

### Requirement: rejeitar senha incorreta
O sistema SHALL interromper o login quando a validação de senha retornar falso.

#### Scenario: senha incorreta
- **WHEN** o verificador retorna falso
- **THEN** nenhum token é emitido

#### Scenario: senha correta
- **WHEN** o verificador retorna verdadeiro
- **THEN** o login continua para criar o token
