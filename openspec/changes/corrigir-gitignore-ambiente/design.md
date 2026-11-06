# Design

## Context

O `.gitignore` atual exclui `.venv/`, mas o README orienta criar `.venv-cashsave`.
Também exclui apenas `.env`, deixando variantes locais como `.env.local` sem uma
regra explícita. Os diretórios `.web`, `.states` e `__pycache__` já têm regras,
algumas duplicadas.

## Goals / Non-Goals

**Goals:**
- Ignorar o ambiente virtual descrito no README e nomes comuns de ambientes
  Python locais.
- Ignorar arquivos `.env` e suas variantes em qualquer diretório, mantendo
  `.env.example` rastreável.
- Preservar as exclusões existentes e remover duplicatas desnecessárias.

**Non-Goals:**
- Remover do índice arquivos que já estejam rastreados pelo Git.
- Alterar arquivos do usuário, segredos ou configurações globais do Git.
- Ignorar todo e qualquer arquivo compactado do repositório.

## Decisions

- Adicionar regras explícitas para `.venv-cashsave/` e `venv/` em vez de uma
  regra ampla que poderia ocultar diretórios não relacionados.
- Cobrir `.env` e `.env.*` em qualquer nível, com exceção explícita para
  `.env.example`.
- Preservar as regras de build, cache, banco de dados e arquivos compactados
  que já existem; consolidar apenas as entradas duplicadas.
- Verificar os padrões com `git check-ignore` e confirmar que `.env.example`
  não é ignorado.

## Risks / Trade-offs

- [Risk] Arquivos secretos já rastreados continuam no índice → esta mudança
  configura apenas novos arquivos e não remove conteúdo histórico.
- [Risk] Uma exceção mal posicionada pode ignorar o modelo de ambiente → testar
  explicitamente `.env.example` junto aos nomes secretos.

## Migration Plan

1. Ajustar as regras do `.gitignore`.
2. Verificar os padrões para ambientes, caches e variantes de `.env`.
3. Executar `git diff --check` e validar a mudança OpenSpec.
