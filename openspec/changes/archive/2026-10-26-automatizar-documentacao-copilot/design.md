# Design: automatizar-documentacao-copilot

## Abordagem

Usar o arquivo de instruções de repositório `.github/copilot-instructions.md`, carregado pelo GitHub Copilot Chat no contexto deste projeto. As instruções direcionam o Copilot a consultar o estado e as especificações OpenSpec, reutilizar uma mudança ativa quando apropriado ou criar uma nova, e manter os artefatos atualizados durante a implementação.

## Limites

As instruções orientam as sessões do Copilot, mas não são um observador de arquivos nem um mecanismo de bloqueio. Alterações manuais e de ferramentas externas não são detectadas nem documentadas automaticamente.

## Verificação

Validar os artefatos da mudança com a CLI OpenSpec. Confirmar também que as instruções estão versionadas no local esperado pelo GitHub Copilot.
