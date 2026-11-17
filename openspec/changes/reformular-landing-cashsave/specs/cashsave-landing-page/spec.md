## Purpose

Definir a experiência pública de apresentação do CashSave, incluindo navegação, demonstrações ilustrativas, informações dos recursos existentes e acessibilidade responsiva.

## ADDED Requirements

### Requirement: apresentação pública responsiva do produto
O sistema SHALL apresentar na rota pública inicial uma página responsiva que comunique a proposta do CashSave, com chamadas claras para cadastro e acesso.

#### Scenario: visitante conhece o CashSave
- **WHEN** uma pessoa abre a rota `/`
- **THEN** a página apresenta o valor do produto, uma ação para começar pelo cadastro e uma ação para acessar uma conta existente

#### Scenario: visitante navega entre seções
- **WHEN** a pessoa usa os links do cabeçalho ou os botões de descoberta
- **THEN** a página navega às seções correspondentes sem sair da landing page

#### Scenario: visitante usa uma tela estreita
- **WHEN** a página é aberta em um smartphone ou tablet
- **THEN** o conteúdo se reorganiza sem rolagem horizontal indesejada e mantém controles confortáveis para toque

### Requirement: demonstrações visuais identificadas
O sistema SHALL distinguir claramente conteúdo e valores ilustrativos de dados financeiros reais, sem persistir ou registrar qualquer informação mostrada nas demonstrações.

#### Scenario: prévia ilustrativa do produto
- **WHEN** a landing page exibe um resumo financeiro ou um gráfico de exemplo
- **THEN** a interface identifica o conteúdo como ilustrativo e não o apresenta como dado de uma conta real

#### Scenario: demonstração estática do Jarvis
- **WHEN** a landing page mostra uma conversa de exemplo entre usuário e Jarvis
- **THEN** a conversa é somente visual e não chama a integração de IA nem cria uma transação

### Requirement: descrição fiel dos recursos
O sistema SHALL apresentar somente funcionalidades já disponíveis no CashSave e SHALL omitir políticas, garantias, estatísticas e informações institucionais que não estejam definidas no produto.

#### Scenario: apresentação de recursos existentes
- **WHEN** uma seção descreve recursos do aplicativo
- **THEN** cada descrição corresponde a funcionalidades disponíveis nas telas existentes

#### Scenario: links institucionais indisponíveis
- **WHEN** o produto não possui uma rota publicada de privacidade ou termos
- **THEN** a landing page não inventa ou anuncia um destino inexistente para esses links

### Requirement: movimento acessível e não essencial
O sistema SHALL usar movimento visual discreto que não seja necessário para acessar conteúdo e SHALL respeitar a preferência de movimento reduzido do sistema operacional.

#### Scenario: movimento reduzido habilitado
- **WHEN** o usuário ativa `prefers-reduced-motion`
- **THEN** animações decorativas e transições da landing page são removidas ou reduzidas substancialmente sem ocultar conteúdo

#### Scenario: navegação por teclado
- **WHEN** o usuário navega pela página com teclado
- **THEN** links e botões permanecem alcançáveis e exibem foco visível
