# secure-login-validation Specification

## Purpose

Garante que o CashSave só emita uma sessão quando a senha enviada corresponder ao hash armazenado para o e-mail informado.

## Requirements

### Requirement: exigir verificação de senha verdadeira

O sistema SHALL continuar a autenticação somente quando o resultado da verificação de senha for explicitamente verdadeiro.

#### Scenario: senha inválida

- **WHEN** o e-mail existe e a senha não corresponde ao hash
- **THEN** o sistema rejeita a solicitação e não emite token

#### Scenario: senha válida

- **WHEN** o e-mail existe e a senha corresponde ao hash
- **THEN** o sistema emite um token de sessão

