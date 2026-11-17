# Proposal

## Why

O acesso ao Jarvis hoje não está disponível de forma consistente no shell compartilhado; o atalho flutuante existente aparece apenas em Preferências. Um acesso rápido persistente nas telas autenticadas reduz o caminho até o assistente sem substituir o menu nem duplicar a experiência de conversa.

## What Changes

- Adicionar ao shell autenticado um botão flutuante circular, acessível e responsivo, com identidade visual própria do Jarvis, tooltip e animações sutis.
- Direcionar o botão para a rota existente `/assistente`, preservando o histórico e o fluxo de conversa atuais.
- Omitir o atalho quando a pessoa não estiver autenticada, já estiver na página do Jarvis ou estiver em Preferências, uma tela de formulário prioritária.
- Respeitar movimento reduzido e manter o botão abaixo de diálogos e sobreposições prioritárias.

## Capabilities

### New Capabilities

### Modified Capabilities

- `authenticated-app-shell`: definir a disponibilidade, acessibilidade e comportamento responsivo do atalho global ao Jarvis.

## Impact

- `CashSave/components/layout.py`: shell compartilhado das páginas autenticadas.
- `CashSave/CashSave.py`: remoção do atalho que hoje está restrito à tela de Preferências.
- `assets/cashsave-theme.css`: estilo, tooltip e animações com suporte a `prefers-reduced-motion`.
- Rota `/assistente` e estado/histórico existentes serão reutilizados; nenhuma integração ou dependência nova é prevista.
