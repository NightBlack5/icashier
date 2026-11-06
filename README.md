# CashSave

Aplicativo de organização financeira desenvolvido com Python e Reflex. A
interface roda localmente, enquanto autenticação e persistência usam um grupo de
APIs Xano configurado por ambiente. O assistente financeiro local com Ollama é
opcional e apenas analítico.

## Funcionalidades

- Landing page, autenticação e cadastro.
- Dashboard financeiro, transações, contas, recorrências, orçamentos, metas e
  contas a pagar.
- Calendário, perfil, preferências e upload de avatar.
- Relatórios de despesas em PDF.
- Assistente Jarvis com histórico e integração opcional com Ollama.
- Definições versionadas de APIs e tabelas em `xano/`.

O estado detalhado de cada funcionalidade, limitações e evidências está em
[`spec/PROJETO.md`](spec/PROJETO.md). O relatório de auditoria histórica está em
[`docs/AUDITORIA_TECNICA.md`](docs/AUDITORIA_TECNICA.md).

## Tecnologias

- Python e Reflex 0.9.12.
- `python-dotenv` para configuração local.
- Xano para autenticação, persistência e APIs financeiras.
- Ollama local opcional para análise financeira.
- `unittest` para testes automatizados.
- ReportLab para relatórios PDF.

## Pré-requisitos

- Python compatível com a versão instalada do Reflex.
- Acesso aos endpoints Xano publicados para testar fluxos autenticados.
- Ollama e um modelo local somente se o assistente for exercitado.

## Instalação e configuração no Windows

```powershell
py -m venv .venv-cashsave
.\.venv-cashsave\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edite `.env` localmente e configure `CASH_SAVE_API_URL` com a URL HTTPS do grupo
CashSave no Xano. Para usar o assistente, ajuste também as variáveis
`CASHSAVE_OLLAMA_*`. Nunca versione o `.env`.

## Executar

```powershell
$env:PYTHONIOENCODING = "utf-8"
reflex run --env prod --single-port
```

Para desenvolvimento com recarga automática, use `reflex run --env dev`.

## Testar e compilar

```powershell
$env:PYTHONIOENCODING = "utf-8"
python -m unittest discover -s tests -v
reflex compile --dry
```

Os testes locais não substituem a validação de cadastro, login, CRUD,
isolamento entre usuários, upload e persistência em um workspace Xano publicado
com uma conta de demonstração isolada.

## Estrutura

```text
CashSave/       Aplicação Reflex, páginas, estado e integrações
tests/          Testes unitários e verificações de rotas/contratos
xano/           APIs e tabelas versionadas do backend
docs/           Relatórios e documentação histórica
spec/           Especificação técnica consolidada do projeto
portfolio/      Materiais de apresentação do projeto
```

## Documentação técnica

Consulte o [Spec do projeto](spec/README.md) para arquitetura, módulos,
integrações, modelo de dados, segurança, testes, limitações e próximos passos.