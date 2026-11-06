# CashSave

## Documentação demonstrativa do produto

**Versão do documento:** 1.0  
**Data de referência:** 5 de novembro de 2026  
**Tipo:** apresentação funcional, técnica e operacional

> Esta documentação descreve o que está implementado ou explicitamente
> definido no repositório. Quando um fluxo depende do workspace remoto do
> Xano, de uma conta de teste ou de um serviço opcional, isso é indicado
> claramente. Não são tratados como recursos disponíveis os itens que ainda
> estão em configuração, não foram verificados ponta a ponta ou aparecem no
> projeto apenas como sugestão.

## Sumário

1. [Apresentação](#1-apresentação)
2. [Funcionalidades](#2-funcionalidades)
3. [Interface e navegação](#3-interface-e-navegação)
4. [Demonstração prática](#4-demonstração-prática)
5. [Tecnologias utilizadas](#5-tecnologias-utilizadas)
6. [Instalação e utilização](#6-instalação-e-utilização)
7. [Segurança e desempenho](#7-segurança-e-desempenho)
8. [Próximos passos](#8-próximos-passos)
9. [Limitações e evidências](#9-limitações-e-evidências)

---

## 1. Apresentação

### 1.1 Nome e proposta

**CashSave** é um aplicativo web de organização financeira pessoal. A
interface é executada localmente com Reflex e os dados de autenticação e
finanças são consumidos por um grupo de APIs Xano configurado no ambiente.

O produto reúne registro de receitas e despesas, contas, vencimentos,
recorrências, orçamentos, metas e uma visão consolidada da vida financeira em
um único lugar. Também oferece o **Jarvis**, um assistente financeiro de caráter
educativo.

### 1.2 Objetivo principal

Ajudar o usuário a:

- entender quanto recebe, gasta e tem disponível no mês;
- registrar movimentações com valores em reais;
- acompanhar contas a pagar e seus vencimentos;
- criar limites de orçamento e objetivos financeiros;
- transformar os próprios dados em uma visão mais compreensível e acionável.

### 1.3 Problema que procura resolver

O CashSave procura reduzir a dispersão de informações financeiras em anotações,
planilhas e lembretes separados. A proposta é oferecer uma rotina simples de
registro, acompanhamento e educação financeira, sem se apresentar como
aconselhamento profissional.

### 1.4 Público-alvo

- pessoas que desejam começar a organizar as finanças pessoais;
- usuários que precisam acompanhar receitas, despesas e vencimentos;
- pessoas que querem visualizar metas e orçamentos;
- usuários interessados em uma assistente educativa baseada nos próprios dados.

O aplicativo não substitui um profissional financeiro e não foi identificado
como sistema bancário, corretora ou ferramenta de aconselhamento regulado.

---

## 2. Funcionalidades

### 2.1 Visão geral das funcionalidades

| Funcionalidade | Situação | Como funciona |
|---|---|---|
| Landing page | Concluída no código | Apresenta a proposta, recursos e chamadas para login/cadastro. |
| Cadastro e login | Implementados; E2E remoto pendente | Validam campos localmente e usam `auth/signup` e `auth/login` do Xano. |
| Dashboard | Implementado; depende de sessão e dados Xano | Exibe saldo mensal, receitas, despesas, contas próximas, gráfico, notificações e atalhos. |
| Transações | Implementadas; dependem de Xano publicado | Permitem criar e excluir receitas/despesas, filtrar e pesquisar. |
| Contas e categorias | Implementadas; dependem de Xano publicado | Permitem cadastrar contas e categorias usadas nos lançamentos. |
| Contas a pagar | Implementadas; dependem de Xano publicado | Permitem registrar, pagar e excluir contas com vencimento. |
| Recorrências | Implementadas no cliente e nas definições Xano | Permitem criar, ativar/desativar e excluir lançamentos recorrentes. |
| Orçamentos | Implementados; dependem de Xano publicado | Registram limite, período e categoria para acompanhamento. |
| Metas financeiras | Implementadas; dependem de Xano publicado | Registram objetivo, data-alvo e contribuições, com progresso calculado. |
| Calendário financeiro | Implementado; depende dos dados carregados | Mostra o mês, permite navegar entre meses e lista próximas contas. |
| Preferências | Implementadas; dependem de Xano publicado | Alteram moeda, localidade, fuso e opções de notificações disponíveis. |
| Avatar | Implementado; upload remoto não verificado | Valida PNG/JPEG/WebP, tamanho e assinatura básica antes do envio ao Xano. |
| Jarvis | Implementado com limites e dependências explícitos | Responde perguntas, mantém histórico local limitado e pode tratar comandos de lançamentos/contas. |
| Relatório PDF | Implementado | Gera relatório de despesas com data, descrição, categoria e total. |
| Exportação CSV | Implementada no estado do app; disponibilidade visual deve ser confirmada | Prepara dados de transações para exportação e protege células contra fórmulas. |
| Suporte e FAQ | Concluídos como conteúdo | Apresenta perguntas frequentes, e-mail e WhatsApp. |
| Apoiar via Pix | Tela concluída; pagamento não configurado | Exibe QR Code/chave somente se os arquivos e valores de configuração existirem. |

### 2.2 Autenticação e sessão

O cadastro solicita nome, e-mail, telefone, senha, confirmação e aceite dos
termos. A validação local exige telefone com DDD, senhas iguais e senha com
pelo menos oito caracteres, uma letra e um número. O login normaliza o e-mail,
envia as credenciais ao Xano e exige um token de sessão na resposta.

Rotas protegidas carregam os dados apenas quando existe sessão. Uma sessão
expirada limpa o estado local e direciona o usuário de volta ao login.

### 2.3 Dashboard

Após o login, a visão geral apresenta:

- saldo do mês;
- total de receitas;
- total de despesas;
- total de contas a pagar nos próximos sete dias;
- notificações dispensáveis;
- sugestões financeiras calculadas localmente;
- gráfico/resumo financeiro;
- próximos vencimentos;
- atalhos para Jarvis, finanças, calendário e nova transação.

O carregamento tenta usar o endpoint consolidado `resumo` e possui fallback
para endpoints individuais quando a resposta não contém todas as coleções
esperadas.

### 2.4 Finanças

Na tela **Finanças**, o usuário pode:

1. escolher entre despesa e receita;
2. informar descrição, valor e data;
3. salvar o lançamento;
4. pesquisar pela descrição;
5. filtrar por tipo e, no estado da aplicação, por período, categoria e conta;
6. excluir transações;
7. acompanhar receitas, despesas e saldo estimado;
8. consultar um resumo de orçamentos e metas;
9. gerenciar contas, categorias, recorrências e metas pelos controles
   disponíveis na tela/estado.

Os valores são tratados em centavos no modelo de dados e formatados em reais
para a interface.

### 2.5 Contas a pagar e calendário

O calendário permite navegar por mês e destaca o dia atual. O painel
**Próximas Contas** permite informar descrição, valor e vencimento. Uma conta
pendente pode ser marcada como paga ou excluída.

As recorrências suportam tipos de receita/despesa, frequência mensal ou anual,
próxima data e ativação/desativação. O processamento de recorrências depende
da publicação correspondente no Xano.

### 2.6 Orçamentos e metas

Orçamentos possuem nome, limite, período inicial/final e categoria. Metas
possuem nome, valor objetivo, data-alvo e contribuição. O estado local calcula
percentuais de progresso e alimenta os cards de planejamento.

### 2.7 Jarvis: assistente financeiro

O Jarvis é uma assistente de apoio e educação financeira. O fluxo observado
inclui:

- perguntas sobre receitas, despesas, economia, metas e orçamento;
- histórico de até oito conversas, com até vinte mensagens por conversa,
  armazenado no `LocalStorage` do navegador;
- contexto montado a partir dos dados financeiros carregados do usuário;
- cálculo local de totais, totais mensais, despesas por categoria, orçamentos,
  metas e projeções;
- projeção marcada como estimativa e considerada insuficiente com menos de
  dois meses de transações;
- geração de relatório PDF quando a mensagem solicita um relatório de gastos;
- interpretação de lançamentos em linguagem natural para receitas e despesas,
  com confirmação antes da gravação;
- interpretação de contas a pagar, solicitando dados ausentes antes de criar;
- rejeição de comandos incompletos, valores inválidos e operações sem sessão.

A IA não recebe o token de autenticação no contexto, não executa SQL/código e
não tem autorização para fazer operações financeiras arbitrárias.

#### Ollama opcional

Quando configurado, o backend pode consultar um modelo Ollama local em
`127.0.0.1:11434`. O navegador não acessa diretamente o Ollama. Sem o serviço,
o aplicativo continua iniciando e informa que a integração local está
indisponível. O projeto não baixa modelos automaticamente.

### 2.8 Áreas públicas

- **Sobre:** explica a proposta educacional, os recursos e o caráter não
  profissional da orientação.
- **Suporte:** FAQ, e-mail, WhatsApp e cartões de redes sociais; os links de
  Instagram e TikTok estão como placeholders (`#`).
- **Apoiar o CashSave:** apresenta apoio opcional via Pix. No estado atual do
  repositório, a chave Pix está vazia e o QR Code só aparece se o arquivo
  correspondente estiver configurado.

### 2.9 Classificação de entrega

#### Concluído no código

As telas, rotas, eventos de estado, validações locais, cálculos, handlers de
CRUD, geração de PDF, histórico local do Jarvis e definições versionadas de
APIs/tabelas estão presentes no repositório. Os testes unitários cobrem
diversos desses comportamentos.

#### Incompleto ou não verificado

- fluxo autenticado real contra um workspace Xano publicado;
- persistência real após reinício, isolamento entre contas e upload de avatar
  em ambiente remoto;
- execução real com modelo Ollama nesta máquina;
- configuração de QR Code e chave Pix;
- links de Instagram e TikTok;
- exportação de planilha mencionada no FAQ como “em breve”;
- alertas externos/push: o código possui preferências e notificações na
  interface, mas não comprova envio externo;
- suporte a banco local/offline, que não existe: o app depende de internet e
  Xano para carregar/salvar dados.

#### Planejado ou sugerido, não disponível

Como próximos incrementos, podem ser considerados exportação de planilha
completa, alertas externos, integração bancária, parcelamento, transferência
entre contas, reconciliação, melhorias de relatórios e publicação de contratos
operacionais. Esses itens são sugestões e não devem ser apresentados como
funcionalidades atuais.

---

## 3. Interface e navegação

### 3.1 Rotas

| Rota | Tela | Acesso |
|---|---|---|
| `/` | Landing page | Público |
| `/login` | Login | Público |
| `/cadastro` | Cadastro | Público |
| `/app` | Visão Geral | Protegido |
| `/assistente` | Jarvis | Protegido |
| `/financas` | Finanças | Protegido |
| `/calendario` | Calendário Financeiro | Protegido |
| `/perfil` | Preferências/perfil | Protegido |
| `/sobre` | Sobre | Público |
| `/suporte` | Central de Suporte | Público |
| `/apoiar` | Apoiar o CashSave | Público |

### 3.2 Elementos visuais principais

- **Landing:** marca CashSave, navegação por âncoras, chamada principal,
  prévia ilustrativa do painel, recursos e seção “Como funciona”.
- **Área autenticada:** sidebar fixa com Visão Geral, Jarvis, Finanças,
  Calendário, Preferências, Sobre, Suporte e Apoiar; avatar/nome do usuário e
  botão Sair.
- **Visão Geral:** cards de indicadores, notificações, gráfico, vencimentos,
  atalhos e banner do Jarvis.
- **Finanças:** cartões de totais, formulário de nova transação, planejamento e
  lista filtrável.
- **Calendário:** grade mensal de sete colunas e painel de contas.
- **Jarvis:** conversas, mensagens, entrada de texto, nova conversa e histórico.
- **Perfil:** dados de perfil, avatar e preferências disponíveis no estado.

### 3.3 Capturas de tela

Não há capturas de tela reais (`PNG`, `JPG` ou `WEBP`) versionadas no
repositório. Por isso, este documento não apresenta imagens inventadas. Há um
asset decorativo de fundo de login em
[`assets/login-background.svg`](../assets/login-background.svg), mas ele não é
uma captura da aplicação. Para uma apresentação comercial, recomenda-se gerar
capturas em um ambiente com conta de demonstração isolada e Xano publicado.

---

## 4. Demonstração prática

### 4.1 Abertura pública

1. Inicie o CashSave conforme a seção de instalação.
2. Abra o endereço local informado pelo Reflex, normalmente
   `http://localhost:3000`.
3. Na landing page, observe a proposta, os recursos e os botões **Acessar** ou
   **Começar grátis**.
4. Use **Sobre** para conhecer o objetivo educativo e **Suporte** para abrir o
   FAQ.

### 4.2 Cadastro e entrada

1. Acesse `/cadastro`.
2. Informe nome, e-mail, telefone, senha, confirmação e aceite os termos.
3. Envie o cadastro. O Xano deve retornar um token de sessão.
4. Alternativamente, acesse `/login`, informe e-mail e senha e entre.
5. Após autenticar, a aplicação carrega `/resumo` e os dados financeiros.

> Esta etapa requer endpoints Xano realmente publicados e uma conta de
> demonstração. O código local não comprova a operação do workspace remoto.

### 4.3 Registro de uma despesa

1. Na Visão Geral, abra **Finanças**.
2. Em **Nova transação**, mantenha o tipo **despesa**.
3. Digite, por exemplo, `Supermercado`, `250,00` e a data.
4. Salve e atualize os dados.
5. Confira o total de despesas, o saldo estimado e a lista de transações.
6. Use a busca ou o filtro de tipo para localizar o lançamento; use excluir
   apenas se desejar removê-lo.

### 4.4 Conta a pagar

1. Abra **Calendário**.
2. Informe descrição, valor e vencimento em **Próximas Contas**.
3. Adicione a conta.
4. Navegue pelos meses para visualizar o calendário.
5. Quando o pagamento ocorrer, clique em **Pagar**; a conta deixa de ser
   pendente conforme a resposta do backend.

### 4.5 Orçamento e meta

1. Em **Finanças**, crie um orçamento com nome, limite, período e categoria.
2. Crie uma meta com objetivo, data-alvo e contribuição.
3. Registre novas transações e contribuições.
4. Observe o resumo de planejamento e o percentual de progresso.

### 4.6 Pergunta ao Jarvis

1. Abra **Jarvis**.
2. Pergunte, por exemplo: “Quanto gastei este mês?” ou “Como posso economizar
   em alimentação?”.
3. O sistema monta o contexto com os dados já carregados e responde com
   análise educativa.
4. Para criar um lançamento, use uma mensagem explícita e confirme os dados
   antes da gravação.
5. Para gerar um relatório, peça um PDF de gastos; o resultado é um arquivo
   gerado no servidor com despesas e total.

### 4.7 Encerramento

Clique em **Sair** na barra lateral. A sessão local é limpa e as rotas
protegidas voltam a exigir autenticação.

---

## 5. Tecnologias utilizadas

| Categoria | Tecnologia | Uso identificado |
|---|---|---|
| Linguagem | Python | Estado, páginas, componentes, integração HTTP e regras de negócio. |
| Framework web | Reflex `0.9.12` | UI, rotas, estado reativo, eventos e servidor da aplicação. |
| Componentes visuais | Radix Themes | Tema escuro, componentes e tokens visuais. |
| Estilização | Tailwind v4 plugin do Reflex | Plugin de estilo configurado no `rxconfig.py`. |
| Configuração | `python-dotenv` | Leitura de variáveis de ambiente. |
| Relatórios | ReportLab | Geração do PDF de despesas. |
| HTTP | `urllib.request` e JSON da biblioteca padrão | Comunicação do cliente com Xano e Ollama. |
| Backend remoto | Xano | Autenticação, tabelas, APIs e persistência financeira. |
| IA local opcional | Ollama | Respostas do modelo local, quando configurado. |
| Armazenamento no navegador | Cookies e `LocalStorage` via Reflex | Sessão, e-mail lembrado, notificações dispensadas e histórico do Jarvis. |

### 5.1 Dados e tabelas

As definições versionadas em `xano/table/` incluem usuários, transações,
contas, categorias, contas a pagar, recorrências, orçamentos, metas,
preferências e conversas/mensagens do assistente. O aplicativo não usa SQLite,
SQLModel ou outro banco local para persistir os dados financeiros.

### 5.2 APIs e integrações

O grupo `cashsave` do Xano possui rotas para autenticação, resumo, transações,
contas, categorias, contas a pagar, recorrências, orçamentos, metas,
preferências, avatar e conversas. A publicação das definições em `xano/` é uma
etapa operacional separada e não é comprovada apenas pela existência dos
arquivos no Git.

---

## 6. Instalação e utilização

### 6.1 Requisitos

- Windows com Python disponível;
- acesso à internet;
- workspace Xano com o grupo `cashsave` publicado;
- conta válida para testar fluxos autenticados;
- Ollama e um modelo compatível apenas se o Jarvis local for utilizado.

### 6.2 Instalação no Windows

No PowerShell, na raiz do projeto:

```powershell
py -m venv .venv-cashsave
.\.venv-cashsave\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Configure um `.env` local, sem versioná-lo:

```dotenv
CASH_SAVE_API_URL=<URL_DO_GRUPO_CASHSAVE_NO_XANO>
CASH_SAVE_COOKIE_SECURE=false
CASHSAVE_OLLAMA_BASE_URL=http://127.0.0.1:11434
CASHSAVE_OLLAMA_MODEL=llama3.2:3b
CASHSAVE_OLLAMA_TIMEOUT=20
```

Use uma URL local para Ollama. O cliente valida que a integração seja local e
não deve ser apontada para um serviço remoto não autorizado.

### 6.3 Execução

Para executar localmente:

```powershell
$env:PYTHONIOENCODING = "utf-8"
reflex run --env prod --single-port
```

Para desenvolvimento com recarga automática, use `--env dev`. A porta deve
ser confirmada no log do Reflex; o README indica `http://localhost:3000` como
valor habitual, não como garantia.

### 6.4 Publicação do Xano

Publique as definições específicas de `xano/api/cashsave/` e `xano/table/` no
grupo `cashsave`. Não use os arquivos de exemplo em
`xano/api/authentication/`. Confirme especialmente login, signup, `auth/me`,
`resumo` e as rotas de recorrência, além de filtros por `$auth.id`.

### 6.5 Verificações

```powershell
$env:PYTHONIOENCODING = "utf-8"
python -m unittest discover -s tests -v
reflex compile --dry
```

Os testes locais não substituem teste autenticado de ponta a ponta, publicação
do Xano, confirmação de isolamento entre usuários ou execução real do Ollama.

---

## 7. Segurança e desempenho

### 7.1 Mecanismos identificados

- autenticação remota pelo Xano;
- token mantido em cookie Reflex `cashsave_auth`;
- cookie configurado com `SameSite=Strict`, validade de 24 horas e flag
  `secure` controlada por ambiente;
- chamadas autenticadas enviam o token como Bearer;
- rotas protegidas exigem sessão antes do carregamento;
- endpoints versionados usam autenticação de usuário e filtros pelo usuário;
- valores monetários persistidos em centavos;
- conversão monetária usa `Decimal` e arredondamento explícito;
- senha validada localmente antes do cadastro;
- upload de avatar limita extensão, assinatura básica e tamanho de 5 MB;
- texto exportado para CSV é protegido contra fórmulas;
- token não é incluído no contexto enviado ao assistente;
- URL do Ollama é validada para uso local;
- mensagens de erro de API são convertidas para mensagens de usuário, sem
  expor detalhes do provedor.

### 7.2 Desempenho e comportamento de carregamento

- o resumo consolidado reduz várias chamadas quando contém todas as coleções;
- há fallback para chamadas individuais quando o resumo é incompleto;
- o estado evita recarregar dados já carregados, salvo atualização forçada;
- histórico do Jarvis possui limites para quantidade de conversas e mensagens;
- o relatório PDF é gerado em memória;
- cálculos de totais, categorias, metas e projeções são realizados localmente
  sobre os dados carregados.

### 7.3 Limites de comprovação

O repositório não comprova HTTPS, CSP, CORS, proxy, WebSocket, configuração
final de cookies no ambiente publicado, backups, restauração, transações
atômicas do Xano ou auditoria de dependências contra uma base externa. Essas
verificações precisam ocorrer no ambiente de implantação.

---

## 8. Próximos passos

Os itens abaixo são recomendações ou planos possíveis, não funcionalidades
disponíveis nesta versão:

1. publicar e validar os endpoints Xano em um ambiente de demonstração isolado;
2. executar testes E2E de cadastro, login, CRUD, logout, expiração e isolamento
   entre usuários;
3. configurar capturas de tela reais e um roteiro de demonstração reproduzível;
4. concluir exportação para planilha;
5. configurar Pix, Instagram e TikTok;
6. decidir e implementar notificações externas de vencimento, orçamento e meta;
7. documentar contratos de payload/resposta das APIs;
8. adicionar relatórios com filtros e histórico;
9. avaliar transferências, parcelamento, reconciliação e integração bancária;
10. monitorar latência e erros das chamadas Xano/Ollama em produção.

---

## 9. Limitações e evidências

As conclusões deste documento foram baseadas no código Python, nas páginas e
componentes Reflex, nas definições versionadas do Xano, no
[`README.md`](../README.md), no
[`docs/AUDITORIA_TECNICA.md`](./AUDITORIA_TECNICA.md), nos testes em `tests/` e
na configuração em [`rxconfig.py`](../rxconfig.py).

Durante a preparação desta documentação, o comando `openspec list` indicou
mudanças ainda ativas relacionadas a autenticação, avatar, Jarvis, calendário,
suporte, navegação e auditoria. Isso reforça a necessidade de separar
“implementado no repositório” de “validado em produção”.

No ambiente de análise desta documentação:

- a suíte de testes não foi concluída porque as dependências do projeto não
  estavam instaladas no interpretador disponível;
- `reflex compile --dry` não pôde ser executado porque o comando `reflex` não
  estava disponível no PATH;
- não havia conta de demonstração nem acesso administrativo ao workspace Xano;
- não havia comando Ollama disponível;
- não havia capturas de tela reais versionadas.

Essas limitações não alteram o código do aplicativo, mas devem ser resolvidas
antes de apresentar os fluxos autenticados como uma demonstração ponta a ponta.
