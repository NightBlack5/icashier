# Proposta: configurar-ambiente-reflex

## Why

A disciplina pede a inicialização do projeto e a configuração do ambiente com Reflex. Sem essa base não é possível construir as telas nem integrar o backend.

## What Changes

- Inicializar o projeto Reflex (`reflex init`).
- Criar o ambiente virtual `.venv`.
- Registrar as dependências em `requirements.txt` com o Reflex em versão fixa.

Fora do escopo desta mudança: telas, navegação, Xano e controle de versão (mudanças próprias).

## Capabilities

### New Capabilities
- `reflex-environment`: Garantir que o projeto CashSave tenha o ambiente Python e Reflex configurado e possa ser executado localmente.

### Modified Capabilities
- Nenhuma.

## Impact

- Projeto: CashSave (Python + Reflex, backend em Xano).
- Referência visual: capturas da versão antiga (Base44). Nenhum código copiado.
