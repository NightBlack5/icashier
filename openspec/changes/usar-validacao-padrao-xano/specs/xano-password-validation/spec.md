# Spec Delta

## Purpose

Garante que o endpoint de login somente emita token quando o verificador de senha do Xano confirmar as credenciais enviadas.

## ADDED Requirements

### Requirement: exigir senha validada pelo Xano
O sistema SHALL usar diretamente o resultado verdadeiro da verificação de senha como condição para continuar o login.

#### Scenario: senha inválida
- **WHEN** o verificador retorna falso
- **THEN** a precondition interrompe a execução e nenhum token é emitido

#### Scenario: senha correta
- **WHEN** o verificador retorna verdadeiro
- **THEN** a execução continua e um token é emitido
