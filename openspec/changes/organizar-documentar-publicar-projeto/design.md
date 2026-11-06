# Design

## Escopo isolado

O trabalho será limitado a documentação nova, atualização do README e validações
não destrutivas. Não serão editados arquivos que já estavam modificados no início
da missão, incluindo módulos Python, `.gitignore`, mudanças OpenSpec existentes e
artefatos do portfólio.

## Fontes de verdade

- `requirements.txt` para dependências Python declaradas.
- `rxconfig.py` para configuração Reflex.
- `CashSave/CashSave.py` para registro de páginas e composição da aplicação.
- `CashSave/state.py` e `CashSave/ai_services.py` para estado e integrações.
- `xano/` para contratos versionados de API e tabelas.
- `tests/` para cobertura local existente.
- `.env.example` somente para nomes de configuração; o `.env` local não será
  lido, copiado ou versionado.

## Documentação

`spec/README.md` será o índice e `spec/PROJETO.md` conterá a visão geral,
arquitetura, diretórios, tecnologias, fluxos, dados, configuração, testes,
segurança, limitações e roadmap. Cada item distinguirá implementado, parcial,
planejado ou não verificado.

## Publicação segura

Antes do commit será executado `git diff --cached --name-status` após adicionar
somente os paths desta missão. Se qualquer arquivo preexistente aparecer no
índice, a publicação será interrompida. O push usará a branch atual e nunca
`--force`.
