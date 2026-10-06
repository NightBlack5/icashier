# Design: configurar-ambiente-xano

## Context

O backend e o banco de dados do CashSave serão feitos em Xano, por exigência da disciplina. Antes de criar tabelas e APIs é preciso ter o ambiente de trabalho com o Xano funcionando.

## Decisions

1. O workspace usado neste momento é pessoal (plano gratuito). A decisão sobre usar um workspace único do grupo fica para a Change de integração.
2. O plano gratuito não tem sandbox: as mudanças serão enviadas direto ao workspace, sempre com `--dry-run` antes.
3. O código do Xano fica na pasta `xano/` e é versionado com Git; chaves e tokens nunca entram no repositório.

## Risks / Trade-offs

Plano gratuito com limite de requisições e sem sandbox.

Nota de processo: esta mudança foi documentada em formato OpenSpec depois de a implementação já ter sido feita. As mudanças seguintes seguem a ordem proposta, specs, design, tarefas e só então código.
