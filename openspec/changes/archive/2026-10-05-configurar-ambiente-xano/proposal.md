# Proposta: configurar-ambiente-xano

## Why

O backend e o banco de dados do CashSave serão feitos em Xano, por exigência da disciplina. Antes de criar tabelas e APIs é preciso ter o ambiente de trabalho com o Xano funcionando.

## What Changes

- Instalar o Xano CLI.
- Autenticar com `xano auth` e definir o workspace no perfil.
- Fazer o pull inicial do workspace para a pasta `xano/`.
- Configurar o Xano Developer MCP no VS Code.

Fora do escopo desta mudança: criação de tabelas, endpoints e a integração do Reflex com a API (mudanças futuras).

## Capabilities

### New Capabilities
- `xano-environment`: Configurar o Xano CLI e a conexão com o workspace para que o código do backend possa ser baixado e versionado.

### Modified Capabilities
- Nenhuma.

## Impact

- Projeto: CashSave (Python + Reflex, backend em Xano).
- Referência visual: capturas da versão antiga (Base44). Nenhum código copiado.
