# Tasks

## 1. Persistência do estado

- [x] 1.1 Adicionar armazenamento local JSON para as conversas e normalizar registros válidos ao carregar; verificar com testes unitários para conteúdo válido, ausente e inválido.
- [x] 1.2 Persistir conversas concluídas e restaurar a conversa selecionada ao abrir o Jarvis, preservando os limites de oito conversas e vinte mensagens; verificar com testes de estado.

## 2. Integração e validação

- [x] 2.1 Validar o change com `openspec validate persistir-historico-conversas-jarvis` e compilar com `python -m reflex compile --dry`.
