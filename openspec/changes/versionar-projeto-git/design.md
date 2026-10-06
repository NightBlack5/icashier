# Design: versionar-projeto-git

## Context

O projeto precisa de histórico de alterações e de um repositório compartilhado pelo grupo. Também é preciso impedir que ambientes virtuais, arquivos gerados e credenciais sejam enviados.

## Decisions

1. As pastas `backend.zip` e `frontend.zip` são referência da versão antiga e ficam fora do repositório (a confirmar com o grupo).
2. A pasta `xano/` é versionada, pois contém o código do backend.
