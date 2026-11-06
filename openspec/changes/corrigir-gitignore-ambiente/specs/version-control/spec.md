# Spec Delta

## MODIFIED Requirements

### Requirement: Arquivos ignorados

O arquivo `.gitignore` SHALL excluir ambientes Python locais (`.venv/`,
`.venv-cashsave/`, `venv/`), arquivos de configuração secretos `.env` e
variantes (`.env.*`), exceto o modelo seguro `.env.example`, além de `.web/`,
`.states/`, `__pycache__/`, bancos de dados locais, logs e arquivos compactados
gerados pelo projeto.

#### Scenario: Status limpo

- **WHEN** o desenvolvedor executa `git status` depois de criar um ambiente
  virtual local e arquivos de configuração `.env`
- **THEN** esses arquivos locais ou secretos não aparecem como alterações
  rastreáveis, enquanto `.env.example` continua disponível para versionamento
