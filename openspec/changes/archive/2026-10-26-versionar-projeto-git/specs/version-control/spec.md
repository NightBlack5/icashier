## Purpose

Versionar o projeto com Git e mantê-lo em um repositório remoto, sem arquivos pesados nem segredos.

## ADDED Requirements

### Requirement: Repositório Git inicializado
O projeto SHALL ter um repositório Git na raiz com pelo menos um commit.

#### Scenario: Primeiro commit
- **WHEN** o desenvolvedor executa `git log` na raiz do projeto
- **THEN** ao menos um commit é exibido

### Requirement: Arquivos ignorados
O arquivo `.gitignore` SHALL excluir `.venv/`, `.web/`, `.states/`, `__pycache__/` e arquivos `.env`.

#### Scenario: Status limpo
- **WHEN** o desenvolvedor executa `git status` depois do primeiro commit
- **THEN** nenhum arquivo ignorado aparece como alteração

### Requirement: Segredos fora do repositório
Tokens, chaves e credenciais SHALL NOT ser versionados.

#### Scenario: Verificação de segredos
- **WHEN** o conteúdo do repositório é revisado antes do envio ao GitHub
- **THEN** nenhum token ou chave aparece nos arquivos versionados
