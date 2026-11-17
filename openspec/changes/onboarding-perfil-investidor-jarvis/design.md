# Design: onboarding e perfil do investidor

A arquitetura atual do CashSave já concentra estado compartilhado em `AppState`, com persistência em cookie e `LocalStorage`. A nova funcionalidade usa essa estrutura para salvar progresso do onboarding sem criar uma segunda IA ou duplicar dados financeiros.

## Estrutura

- `AppState` recebe armazenamento local para respostas do onboarding e avaliações do perfil de investidor.
- O painel de onboarding fica integrado à página de preferências, com etapas numeradas e ações de avançar, voltar e pular.
- A avaliação do perfil usa as respostas coletadas para calcular uma classificação com base em tolerância ao risco, conhecimento, experiência, objetivos e horizonte de investimento.
- A tela de perfil de investidor reutiliza os mesmos dados e explica a classificação de forma educacional, sem apresentar uma recomendação definitiva.
- O layout compartilhado adiciona um botão flutuante do Jarvis no canto inferior direito para manter o assistente sempre acessível.

## Persistência

- O progresso do onboarding é salvo em `LocalStorage` usando JSON.
- O estado do perfil é regenerado sempre que as respostas mudam ou quando o usuário conclui a avaliação.
- Informações não respondidas permanecem como não informadas, sem serem convertidas em zero ou em valores implícitos.

## Limites intencionais

- Não há integração de dados reais de mercado; apenas a estrutura contextual e a lógica de avaliação local.
- As recomendações ficam em nível educativo e não substituem análise profissional ou consultoria regulada.
