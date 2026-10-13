# Proposta: sincronizar-autenticacao-financas

## Por que

Há alterações locais no CashSave e no Xano para cadastro, perfil, transações e funcionalidades financeiras que ainda não estão descritas nas especificações principais. Registrar o comportamento pretendido evita que a documentação fique limitada às primeiras telas do projeto.

## O que muda

- Documentar cadastro, login e gerenciamento da foto de perfil.
- Documentar o resumo financeiro autenticado, os filtros e a exportação de transações.
- Documentar lançamentos recorrentes, metas e notificações financeiras.

Fora do escopo: afirmar que os endpoints Xano já foram publicados ou que os fluxos passaram por teste de ponta a ponta. Essa verificação permanece pendente.

## Capacidades

### Novas capacidades
- `account-access`: cadastro, login e foto do perfil.

### Capacidades modificadas
- `cashsave-finance-data`: resumo autenticado, consulta e exportação de transações, recorrências, metas e notificações.

## Impacto

- Interface e estado em `CashSave/`.
- APIs e tabelas Xano em `xano/`.
- O funcionamento integrado depende de publicar no Xano as alterações locais correspondentes.
