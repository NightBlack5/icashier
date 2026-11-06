# Privacidade da conta

## ADDED Requirements

### Requirement: ocultar e-mail na interface
A interface SHALL exibir nome e avatar, mas não SHALL renderizar o e-mail da
conta autenticada nas áreas internas.

#### Scenario: usuário autenticado navega no app
- **WHEN** uma página interna é aberta
- **THEN** o nome pode ser exibido e o e-mail não aparece no bloco da conta

### Requirement: não enviar e-mail ao contexto da IA
O contexto financeiro SHALL conter somente dados necessários para a análise e
não SHALL conter o e-mail ou credenciais do usuário.

#### Scenario: pergunta financeira
- **WHEN** a assistente monta o contexto para o Ollama
- **THEN** o contexto não contém o e-mail da conta
