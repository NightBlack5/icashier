# Design

## Context

O estado `assistente_conversas` é uma lista transitória do `rx.State`, enquanto os únicos dados persistentes atuais usam `rx.LocalStorage` com strings JSON. A página do Jarvis já executa `carregar_conversas_assistente` ao carregar, mas esse evento não restaura dados.

## Goals / Non-Goals

**Goals:**

- Usar o mesmo padrão de armazenamento local já adotado no estado.
- Validar e normalizar dados lidos do navegador antes de renderizar.
- Persistir somente conversas concluídas e manter os limites atuais.

**Non-Goals:**

- Criar histórico no Xano ou sincronizá-lo entre dispositivos.
- Persistir credenciais, dados financeiros ou mensagens enquanto a resposta ainda está em andamento.

## Decisions

- Adicionar uma chave `LocalStorage` dedicada contendo JSON serializado das conversas.
- Restaurar apenas objetos com `id`, `title` e lista de mensagens no formato esperado; dados inválidos serão ignorados.
- Centralizar a serialização em um método de estado chamado após mutações da lista, evitando divergência entre nova conversa, carregamento e envio.
- Manter o histórico separado por navegador. Xano não será alterado porque o requisito atual é recuperação local no mesmo dispositivo.

## Risks / Trade-offs

- [Risco] O usuário pode limpar o armazenamento do navegador e perder o histórico local. -> Mitigação: deixar o comportamento explícito no escopo local e não tratar dados inválidos como erro fatal.
- [Risco] O armazenamento pode conter dados de versões antigas. -> Mitigação: normalizar e limitar os registros ao restaurar.

## Migration Plan

1. Publicar o estado com a nova chave de armazenamento.
2. Conversas criadas após a atualização serão persistidas automaticamente.
3. Não há migração de dados antigos, pois eles nunca foram armazenados de forma persistente.
4. Para rollback, remover a chave e retornar ao estado transitório anterior.
