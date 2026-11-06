# Implementar IA financeira local com Ollama

## Objetivo

Adicionar uma primeira versão da assistente financeira local do CashSave,
usando Ollama somente pelo backend e reutilizando os dados financeiros já
carregados no `AppState`.

## Escopo da primeira versão

- Cliente HTTP para a API local de chat do Ollama.
- Contexto financeiro mínimo e autorizado, derivado do estado do usuário.
- Cálculos determinísticos de totais, comparações, orçamento, metas e uma
  projeção simples com premissas explícitas.
- Orquestração de perguntas em português com resposta validada e fallback
  explícito quando o Ollama estiver indisponível.
- Histórico local limitado por conversa, sem persistência ou escrita financeira.
- Integração com a tela existente `/assistente`.
- Testes unitários com mocks e documentação de configuração.

## Fora de escopo

- Instalar Ollama ou baixar modelos automaticamente.
- Alterar tabelas ou endpoints Xano.
- Permitir que o modelo execute SQL, código, ferramentas ou operações financeiras.
- Substituir a autenticação existente ou corrigir problemas não necessários para
  a integração local.
