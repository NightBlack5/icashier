# CashSave — especificação técnica

## 1. Visão geral e objetivo

CashSave é uma aplicação web local para organização financeira pessoal. O
objetivo é centralizar registros financeiros, contas, categorias, recorrências,
orçamentos, metas e contas a pagar em uma interface Reflex, com autenticação e
persistência fornecidas por APIs Xano.

## 2. Escopo e estado funcional

| Área | Estado | Evidência ou limite |
|---|---|---|
| Interface Reflex e rotas públicas | Implementado | Páginas em `CashSave/pages/` e registro em `CashSave/CashSave.py` |
| Autenticação e sessão | Parcial | Cliente e contratos Xano existem; fluxo remoto exige workspace e conta de teste |
| Dados financeiros e CRUD | Parcial | APIs e estado existem; persistência remota não foi validada nesta máquina |
| Relatórios PDF | Implementado | `CashSave/expense_reports.py` e dependência ReportLab |
| Assistente Jarvis | Parcial | UI, histórico e integração existem; dependem de Xano |
| Análise local Ollama | Parcial | Serviço opcional e testes mockados; Ollama real não foi executado |
| Segurança e isolamento Xano | Parcial | Contratos versionados usam autenticação/usuário; publicação remota não foi comprovada |
| Publicação web | Não implementado | `reflex run` serve localmente; este repositório não comprova deploy |

## 3. Arquitetura

O Reflex renderiza as páginas e coordena eventos de estado no backend Python.
`CashSave/state.py` concentra estado, validações e chamadas HTTP ao grupo Xano.
`CashSave/ai_services.py` encapsula a integração opcional com Ollama. Os
componentes reutilizáveis ficam em `CashSave/components/`, as páginas em
`CashSave/pages/` e a geração de relatórios em `CashSave/expense_reports.py`.

O fluxo geral é:

```text
navegador -> Reflex/pages -> estado e eventos Python
                         -> APIs Xano -> tabelas Xano
                         -> Ollama local (somente análise, opcional)
```

## 4. Estrutura de diretórios

```text
CashSave/
  CashSave.py              configuração de rotas e composição do app
  state.py                 estado, eventos, validações e cliente Xano
  ai_services.py           serviço Ollama e limites de análise
  expense_reports.py       geração de relatórios PDF
  components/              cards, layout e componentes compartilhados
  pages/                   landing, autenticação e áreas do app
tests/                     testes locais
xano/api/cashsave/         contratos de endpoints
xano/table/                definições de tabelas
docs/                      auditorias e documentação histórica
spec/                      esta especificação consolidada
```

Arquivos gerados como `__pycache__`, ambientes virtuais, perfis temporários do
Chrome e `.env` não fazem parte do produto e não devem ser versionados.

## 5. Tecnologias e dependências

As dependências declaradas em `requirements.txt` são:

- `reflex==0.9.12`: framework de interface, eventos e servidor.
- `python-dotenv`: leitura de configuração local.
- `reportlab`: relatórios PDF.

`rxconfig.py` habilita plugins de sitemap, Tailwind v4 e Radix Themes. A
integração externa usa a biblioteca padrão Python para HTTP/JSON conforme o
estado atual do código.

## 6. Módulos e responsabilidades

| Módulo | Responsabilidade |
|---|---|
| `CashSave/CashSave.py` | Cria o app e registra as rotas |
| `CashSave/state.py` | Sessão, chamadas Xano, estado financeiro, validação e eventos |
| `CashSave/ai_services.py` | Configuração, limites e chamada opcional ao Ollama |
| `CashSave/components/layout.py` | Shell visual e navegação |
| `CashSave/components/cards.py` | Componentes visuais reutilizáveis |
| `CashSave/pages/*.py` | Telas por domínio funcional |
| `CashSave/expense_reports.py` | Relatórios PDF |
| `xano/` | Contratos versionados do backend |

## 7. Fluxos principais

1. A aplicação inicia com `reflex run` e registra as rotas públicas e protegidas.
2. O usuário informa credenciais; o cliente usa o endpoint Xano de login e
   mantém a sessão conforme o estado Reflex.
3. Telas protegidas carregam resumo e recursos financeiros por endpoints Xano.
4. Eventos de criação, edição, exclusão e pagamento validam dados localmente e
   enviam a operação ao backend.
5. O assistente monta contexto de dados já carregados; Ollama, quando
   configurado, responde somente análises e não executa operações financeiras.
6. O relatório de despesas é gerado localmente em PDF.

Os fluxos autenticados e as operações remotas permanecem parciais até serem
executados com um workspace Xano publicado e uma conta isolada.

## 8. APIs e integrações

Os contratos em `xano/api/cashsave/` cobrem autenticação, avatar, categorias,
contas, transações, recorrências, contas a pagar, orçamentos, metas,
preferências, resumo e conversas do assistente. As definições em `xano/table/`
incluem usuários, contas, transações, categorias, recorrências, metas,
orçamentos, contas a pagar, preferências e histórico do assistente.

Variáveis principais:

- `CASH_SAVE_API_URL`: URL HTTPS do grupo de APIs Xano.
- `CASHSAVE_OLLAMA_BASE_URL`: endereço local do Ollama.
- `CASHSAVE_OLLAMA_MODEL`: modelo local escolhido.
- `CASHSAVE_OLLAMA_*`: timeout e limites de pergunta, contexto, histórico,
  resposta e tokens.

## 9. Modelo de dados

O backend versionado separa entidades financeiras por usuário e usa tabelas para
usuários, contas, categorias, transações, recorrências, contas a pagar,
orçamentos, metas, preferências e conversas. Valores monetários são tratados
com conversão explícita e armazenamento em centavos nos contratos relevantes.
O isolamento efetivo depende da publicação correta das APIs Xano.

## 10. Configuração e execução

1. Crie um ambiente virtual.
2. Instale `requirements.txt`.
3. Copie `.env.example` para `.env` e preencha apenas valores locais.
4. Execute `reflex run --env prod --single-port` ou o modo `dev`.
5. Para Ollama, instale o serviço separadamente e baixe um modelo compatível;
   o CashSave não baixa modelos automaticamente.

## 11. Testes e validação

Comandos locais:

```powershell
$env:PYTHONIOENCODING = "utf-8"
python -m unittest discover -s tests -v
reflex compile --dry
```

Os testes cobrem rotas, codificação, formatação monetária, relatórios,
assistente, IA local, autenticação e contratos Xano. O Ollama real, a
persistência remota, o upload e os fluxos autenticados exigem serviços externos
e não são substituídos pelos mocks.

## 12. Segurança

- Segredos devem permanecer em `.env`, nunca em commits.
- O cliente exige URL HTTPS para o grupo Xano.
- O backend versionado usa autenticação e filtros por usuário nos endpoints
  financeiros relevantes.
- Upload de avatar possui validação de extensão, assinatura e limite de tamanho
  conforme a implementação atual.
- O assistente local recebe contexto limitado e não executa SQL, código,
  ferramentas ou operações financeiras.

## 13. Limitações conhecidas

- Não há prova local de que o workspace Xano remoto esteja publicado com os
  contratos presentes neste repositório.
- Não há conta de demonstração isolada disponível para validar todos os fluxos.
- O comando `ollama` não estava disponível no ambiente auditado.
- A execução do Reflex depende de conexão de eventos além da renderização HTTP.
- Perfis temporários e caches locais não são artefatos do produto.

## 14. Próximos passos

- Validar os fluxos autenticados contra um workspace Xano isolado.
- Executar uma verificação de integração com Ollama instalado.
- Automatizar um smoke test HTTP/browser reproduzível no CI.
- Definir o processo de deploy e observabilidade antes de declarar produção.
